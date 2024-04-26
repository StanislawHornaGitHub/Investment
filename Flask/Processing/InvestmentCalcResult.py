"""
.DESCRIPTION
    Class definition for static methods related to Investment refund calculation.
    

.NOTES

    Version:            1.4
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      27-Mar-2024
    ChangeLog:

    Date            Who                     What
    2024-03-31      Stanisław Horna         .calculateAllResults() implemented.
    
    2024-04-01      Stanisław Horna         Handling for refreshing investment results, if previous calculation
                                            ended with incomplete results due to missing fund quotations.
                                            
    2024-04-03      Stanisław Horna         Bugfix in collecting already calculated results.
                                            Response body and code implemented.
                                            
    2024-04-26      Stanisław Horna         Error handling in calculateResult - provided ID does not exist.

"""
import SQL
from SQL.Quotation import Quotation
from SQL.InvestmentResult import InvestmentResult
from SQL.Investment import Investment
from sqlalchemy import func, exc

from sqlalchemy.exc import DatabaseError
import datetime

from Utility import DebugOutput
from Processing.InvestmentConfig import InvestmentConfig

from Utility.Dates import Dates


class InvestmentCalcResult:

    ConvertPeriodNamesDatesToInvestmentResult = {
        "daily": "last_day_result",
        "weekly": "last_week_result",
        "monthly": "last_month_result",
        "yearly": "last_year_result"
    }

    @staticmethod
    def calculateAllResults() -> None:

        # Create session and init processing variables
        session = SQL.base.Session()
        responseCode = 200
        result = {
            "Codes": [],
            "Response": []
        }

        # Get IDs for investments existing in DB
        try:
            investmentsToRefresh = InvestmentConfig.getInvestmentIDs(session)
        except Exception as e:
            session.close()

            return 400, {
                "Status": "Failed to download Investment IDs",
                "Status Details": str(e)
            }

        # Loop through each investment and invoke result calculation
        for id in investmentsToRefresh:

            # invoke investment calculation
            code, responseBody = InvestmentCalcResult.calculateResult(id)

            # append result variable
            result["Codes"].append(code)
            result["Response"].append(responseBody)

        if responseCode == 200:
            if 206 in result["Codes"]:
                responseCode = 206

            if 204 in result["Codes"]:
                responseCode = 204

            if 400 in result["Codes"]:
                responseCode = 400

        # Close SQL session
        session.close()

        return responseCode, result["Response"]

    @staticmethod
    def calculateResult(investment_id: int):

        # Create new SQL session
        session = SQL.base.Session()
        

        try:
            # Check if provided ID exists in DB
            if(Investment.checkInvestmentIDisValid(investment_id, session) != True):
                resultBody = {
                    "Investment ID": investment_id,
                    "Status": f"Investment with ID: {investment_id} does not exist"
                }
                responseCode = 404
                
                return responseCode, resultBody
            
            # Get necessary details required for calculation
            # start date <- oldest date when some fund was bought
            # funds <- list of involved funds
            # ordersMap <- dict of dates and operations
            start_date, funds, ordersMap = InvestmentCalcResult.getInvestmentOrderMap(
                investment_id, session
            )

            # Get quotations for each fund starting from start date of the oldest investment
            quot = InvestmentCalcResult.getFundsQuotation(
                funds, start_date, session
            )

            # Check the latest update, to avoid calculating everything from the beginning
            lastUpdateDate = InvestmentCalcResult.getLastResultDate(
                investment_id, session
            )
        except exc.OperationalError as e:
            resultBody = {
                "Investment ID": investment_id,
                "Status": "Failed to retrieve data from DB",
                "Status_Details": str(e)
            }
            responseCode = 500
            
            return responseCode, resultBody
        
        # Init temp dict for owned participation units
        tempOwnedFunds = {}

        # Check if there is an lastUpdateDate if not, we have to count from the beginning
        if lastUpdateDate == None:

            # Set processing date to start date to begin calculation at day 0
            currentProcessingDate = start_date

            # fill in initiated temp dict
            for fund in funds:
                tempOwnedFunds[fund] = {
                    "ParticipationUnits": 0,
                    "InvestedMoney": 0
                }

        # if there is an lastUpdateDate we can skip already calculated days
        else:
            # Get information about,
            # participation units and invested money for each fund and assign it to temp dict
            for fund in funds:

                LastFundResult = InvestmentCalcResult.getLastFundResult(
                    investment_id,
                    fund,
                    lastUpdateDate,
                    session
                )

                tempOwnedFunds[fund] = {
                    "ParticipationUnits": LastFundResult[0],
                    "InvestedMoney": LastFundResult[1]
                }

            # Increment processing date to the next date as
            # lastUpdateDate is a date retrieved form DB, which means it was already calculated
            currentProcessingDate = Dates.addDays(lastUpdateDate, 1)

            # Get historical data to be able to calculate profits compared to last week, month etc.
            SQLdata = InvestmentResult.getInvestmentResult(
                investment_id, session)

        # Init result variable
        result = []

        # loop through each day until now
        while ((currentProcessingDate <= datetime.datetime.now())):

            # If current date exists in orders map it means that fund was sold or bought
            if currentProcessingDate in list(ordersMap.keys()):

                # Loop through funds to increment participation units and invested money
                for fund in ordersMap[currentProcessingDate]:

                    tempOwnedFunds[fund]["ParticipationUnits"] += (
                        ordersMap[currentProcessingDate][fund]["Money"] /
                        quot[fund][currentProcessingDate]
                    )
                    tempOwnedFunds[fund]["InvestedMoney"] += (
                        ordersMap[currentProcessingDate][fund]["Money"]
                    )

            # Get desired dates to calculate:
            # last day result
            # last week result
            # last month result
            # last year result
            desiredDates = Dates.getDesiredDates(currentProcessingDate)

            # Loop through each fund in investment
            for fund in funds:

                # Try to calculate record entry
                # Try is required if currentProcessingDate is a weekend or bank holiday
                # on such days there is no quotation so any calculation which requires it will fail
                try:
                    record = {
                        "result_date": currentProcessingDate,
                        "investment_id": investment_id,
                        "fund_id": fund,
                        "fund_participation_units": (
                            tempOwnedFunds[fund]["ParticipationUnits"]
                        ),
                        "fund_invested_money": (
                            tempOwnedFunds[fund]["InvestedMoney"]
                        ),
                        "fund_value": (
                            tempOwnedFunds[fund]["ParticipationUnits"] *
                            quot[fund][currentProcessingDate]
                        ),
                        "last_day_result": None,
                        "last_week_result": None,
                        "last_month_result": None,
                        "last_year_result": None
                    }
                except:
                    # If calculation failed, nothing to worry about, just go to next fund
                    # It might be that at current time there is no quotation for particular fund.
                    continue

                # Loop through each time period to calculate appropriate column value
                for date in desiredDates:

                    # Based on the information if lastUpdateDate exists or not,
                    # look up for historical data will be different.
                    # If there is no such date it means that all data we can have is stored in memory,
                    # so we do not have to check the SQL data
                    if lastUpdateDate == None:
                        listToLookUp = [
                            entry for entry in result
                            if entry["fund_id"] == fund
                        ]
                    else:
                        listToLookUp = [
                            entry for entry in (SQLdata + result)
                            if entry["fund_id"] == fund
                        ]

                    # Use Dates method to get entry with required date,
                    # if output is None, it means that there is nothing to count,
                    # as the fund was not bought on desired date yet
                    if ((
                        entryToCompare := Dates.getEntryWithDesiredDate(
                            listToLookUp,
                            "result_date",
                            desiredDates[date]
                        )
                    ) != None) and record["fund_invested_money"] > 0:

                        # If the condition is met we can retrieve destination column name
                        colName = InvestmentCalcResult.ConvertPeriodNamesDatesToInvestmentResult[
                            date]

                        # and try to calculate the result.
                        # try is required as used method can create entries with 0,
                        # for funds which were not bought since the beginning of investment
                        try:
                            record[colName] = (
                                (
                                    (record["fund_value"] - record["fund_invested_money"]) -
                                    (entryToCompare["fund_value"] -
                                     entryToCompare["fund_invested_money"])
                                )
                            )
                        except:
                            # If calculation fails, nothing to worry, fund was not bought yet.
                            pass

                # Append the result list with entry ready to insert to DB
                result.append(record)

            # Calculate next processing date and go to the beginning of while loop
            currentProcessingDate = Dates.addDays(currentProcessingDate, 1)

        # Init processing variables
        responseCode = 200
        resultBody = []

        # Loop through each entry in result var, create an DB entry, add it to session and try to commit.
        for output in result:
            record = InvestmentResult(
                **output
            )
            session.add(record)

        try:
            session.commit()
            resultBody = {
                "Investment ID": investment_id,
                "Status": "Results calculated and added successfully",
                "Last Result Date": Dates.convertDateToString((result[-1]["result_date"]))
            }
        except IndexError as indexErr:

            resultBody = {
                "Investment ID": investment_id,
                "Status": "No new Result to add"
            }
        except Exception as e:

            session.rollback()
            resultBody = {
                "Investment ID": investment_id,
                "Status": "Failed to add results",
                "Status Details": str(e)
            }
            responseCode = 206

        session.close()

        return responseCode, resultBody

    @staticmethod
    def getInvestmentOrderMap(investment_id: int, session):
        resultMap = {}
        fundList = set()
        orders = (
            session
            .query(
                Investment.operation_quotation_date,
                Investment.investment_fund_id,
                Investment.operation_value
            )
            .filter(Investment.investment_id == investment_id)
            .order_by(Investment.operation_quotation_date.asc())
            .all()
        )

        for date, fund_id, money in orders:
            fundList.add(fund_id)
            if date not in list(resultMap.keys()):
                resultMap[date] = {}

            if fund_id not in list(resultMap[date].keys()):
                resultMap[date][fund_id] = {
                    "Money": 0,
                    "ParticipationUnits": 0
                }

            resultMap[date][fund_id]["Money"] += money

        return orders[0][0], list(fundList), resultMap

    @staticmethod
    def getFundsQuotation(fundList: list[str], start_date, session):
        quotation = {}
        for fund in fundList:
            quotation[fund] = InvestmentCalcResult.getQuotation(
                fund, start_date, session)

        return quotation

    @staticmethod
    def getQuotation(fund_id: str, start_date, session):
        result = {}
        quotation = (
            session
            .query(Quotation.date, Quotation.value)
            .filter(Quotation.date >= start_date, Quotation.fund_id == fund_id)
            .all()
        )
        for date, value in quotation:
            result[date] = value

        return result

    @staticmethod
    def getLastResultDate(investment_id, session):
        return InvestmentCalcResult.unifyInvestmentResults(investment_id, session)

    @staticmethod
    def getLastFundResult(investment_id: int, fund_id: str, last_date, session):
        return (
            session
            .query(
                InvestmentResult.fund_participation_units,
                InvestmentResult.fund_invested_money
            )
            .filter(
                InvestmentResult.investment_id == investment_id,
                InvestmentResult.fund_id == fund_id,
                InvestmentResult.result_date == last_date
            )
            .first()
        )

    @staticmethod
    def unifyInvestmentResults(investment_id: int, session) -> datetime.datetime:

        # Create subquery to calculate row number for each fund in investment
        # rank 1 will be assigned to the latest fund's result within investment
        # despite actual result date.
        # It will allow to handle the case when different funds have different latest quotation dates
        subquery = (
            session
            .query(
                InvestmentResult.result_date,
                InvestmentResult.fund_id,
                func.row_number().over(partition_by=(
                    InvestmentResult.investment_id,
                    InvestmentResult.fund_id
                ), order_by=InvestmentResult.result_date.desc()).label('rank')
            )
            .filter(InvestmentResult.investment_id == investment_id)
            .subquery()
        )

        # Find the oldest date with rank 1, so it will contain latest date when each fund of the investment
        # had the same result date.
        dateToFilter = (
            session
            .query(func.min(subquery.c.result_date))
            .filter(
                subquery.c.rank == 1
            )
            .all()
        )[0][0]

        if dateToFilter == None:
            return None

        # Find rows with incomplete results and delete them
        # Example:
        # fund1 has last result from 02.01, but fund2 has result from 05.01,
        # query will delete all funds newer than 02.01,
        # which actually will be result with missing data from some funds
        deletedRecords = (
            session
            .query(InvestmentResult)
            .filter(
                InvestmentResult.investment_id == investment_id,
                InvestmentResult.result_date > dateToFilter
            )
            .delete()
        )
        session.commit()

        # Return the edge date, before which the results are complete
        return dateToFilter
