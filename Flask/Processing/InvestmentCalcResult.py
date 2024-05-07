"""
.DESCRIPTION
    Class definition for static methods related to Investment refund calculation.
    

.NOTES

    Version:            1.6
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
    
    2024-04-30      Stanisław Horna         Add logging capabilities.

    2024-05-06      Stanisław Horna         Add missing I/O datatypes. Refactor variable names.

"""

import datetime
from sqlalchemy import func, orm
from SQL.Quotation import Quotation
from SQL.InvestmentResult import InvestmentResult
from SQL.Investment import Investment
from SQL.write import Session_rw
from SQL.read import Session_ro
from Processing.InvestmentConfig import InvestmentConfig
from Utility.Dates import Dates
from Utility.Logger import logger


class InvestmentCalcResult:

    ConvertPeriodNamesDatesToInvestmentResult = {
        "daily": "last_day_result",
        "weekly": "last_week_result",
        "monthly": "last_month_result",
        "yearly": "last_year_result"
    }

    @staticmethod
    def calculateAllResults() -> tuple[int, list[dict[str, str]]]:

        logger.debug("calculateAllResults()")

        # Create session and init processing variables
        s_ro = Session_ro()
        responseCode = 200
        responseBody = {
            "Codes": [],
            "Response": []
        }

        # Get IDs for investments existing in DB
        try:
            investmentsToRefresh = InvestmentConfig.getInvestmentIDs(s_ro)
        except Exception as e:
            s_ro.close()

            return 400, {
                "Status": "Failed to download Investment IDs",
                "Status Details": str(e)
            }

        # Loop through each investment and invoke result calculation
        for id in investmentsToRefresh:
            logger.debug("Processing investment ID: %s", id)
            # invoke investment calculation
            r_code, r_body = InvestmentCalcResult.calculateResult(id)

            # append result variable
            responseBody["Codes"].append(r_code)
            responseBody["Response"].append(r_body)

        if responseCode == 200:
            if 206 in responseBody["Codes"]:
                responseCode = 206

            if 204 in responseBody["Codes"]:
                responseCode = 204

            if 400 in responseBody["Codes"]:
                responseCode = 400

        # Close SQL session
        s_ro.close()

        logger.debug(
            "calculateAllResults(). Returning body and code: %d",
            responseCode
        )
        return responseCode, responseBody["Response"]

    @staticmethod
    def calculateResult(investment_id: int) -> tuple[int, dict[str, str]]:

        logger.debug("calculateResult(%s)", investment_id)
        # Create new SQL session
        s_rw = Session_rw()
        s_ro = Session_ro()

        try:
            # Check if provided ID exists in DB
            if (Investment.IDisValid(investment_id, s_ro) != True):
                responseCode = 404
                logger.debug(
                    "Provided Investment ID %s does not exist, setting code to %d",
                    investment_id,
                    responseCode
                )
                resultBody = {
                    "Investment ID": investment_id,
                    "Status": f"Investment with ID: {investment_id} does not exist"
                }
                logger.debug(
                    "calculateResult(%s). Returning body and code: %d",
                    investment_id,
                    responseCode
                )
                return responseCode, resultBody

            # Get necessary details required for calculation
            # start date <- oldest date when some fund was bought
            # funds <- list of involved funds
            # ordersMap <- dict of dates and operations
            start_date, funds, ordersMap = InvestmentCalcResult.getInvestmentOrderMap(
                investment_id, s_ro
            )

            # Get quotations for each fund starting from start date of the oldest investment
            quot = InvestmentCalcResult.getFundsQuotation(
                funds, start_date, s_ro
            )

            # Check the latest update, to avoid calculating everything from the beginning
            lastUpdateDate = InvestmentCalcResult.getLastResultDate(
                investment_id, s_rw
            )
        except Exception:
            logger.exception("Exception occurred", exc_info=True)
            resultBody = {
                "Investment ID": investment_id,
                "Status": "Failed to retrieve data from DB",
                "Status_Details": str(e)
            }
            responseCode = 500
            logger.debug(
                "calculateResult(%s). Returning body and code: %d",
                investment_id,
                responseCode
            )
            s_ro.close()
            s_rw.close()
            return responseCode, resultBody

        # Init temp dict for owned participation units
        tempOwnedFunds = {}

        # Check if there is an lastUpdateDate if not, we have to count from the beginning
        if lastUpdateDate is None:

            logger.debug("Last update is none")

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

            logger.debug("Last update is NOT none")

            # Get information about,
            # participation units and invested money for each fund and assign it to temp dict
            for fund in funds:

                LastFundResult = InvestmentCalcResult.getLastFundResult(
                    investment_id,
                    fund,
                    lastUpdateDate,
                    s_ro
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
                investment_id, s_ro)

        logger.debug("Calculating refund")
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

        logger.debug("Adding calculation entries to session")
        # Loop through each entry in result var, create an DB entry, add it to session and try to commit.
        for output in result:
            record = InvestmentResult(
                **output
            )
            s_rw.add(record)

        try:
            s_rw.commit()
            logger.debug("Changes successfully committed")
            resultBody = {
                "Investment ID": investment_id,
                "Status": "Results calculated and added successfully",
                "Last Result Date": Dates.convertDateToString((result[-1]["result_date"]))
            }
        except IndexError as indexErr:
            logger.warning("No new result to add", exc_info=True)
            s_rw.rollback()
            resultBody = {
                "Investment ID": investment_id,
                "Status": "No new Result to add"
            }
        except Exception as e:
            responseCode = 206
            logger.exception("Failed to add entry", exc_info=True)
            s_rw.rollback()
            resultBody = {
                "Investment ID": investment_id,
                "Status": "Failed to add results",
                "Status Details": str(e)
            }

        s_ro.close()
        s_rw.close()
        logger.debug(
            "calculateResult(%s). Returning body and code: %d",
            investment_id,
            responseCode
        )
        return responseCode, resultBody

    @staticmethod
    def getInvestmentOrderMap(
        investment_id: int,
        session: orm.session.Session
    ) -> tuple[
            datetime.datetime,
            list[str],
            dict[
                datetime.datetime,
                dict[
                    str,
                    dict[str, int]
                ]
            ]
    ]:
        resultMap = {}
        fundList = set()
        try:
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
        except:
            logger.exception(
                "getInvestmentOrderMap(%s) failed to retrieve data from DB",
                investment_id,
                exc_info=True
            )
            return None, None, None

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
    def getFundsQuotation(
            fundList: list[str],
            start_date: datetime.datetime,
            session: orm.session.Session
    ) -> dict[
        str,
        dict[datetime.datetime, float]
    ]:
        quotation = {}

        try:
            for fund in fundList:
                quotation[fund] = InvestmentCalcResult.getQuotation(
                    fund, start_date, session)
        except:
            logger.exception(
                "getFundsQuotation(%s, %s) failed to retrieve data from DB",
                str(fundList),
                start_date
            )

        return quotation

    @staticmethod
    def getQuotation(
        fund_id: str,
        start_date: datetime.datetime,
        session: orm.session.Session
    ) -> dict[datetime.datetime, float]:
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
    def getLastResultDate(investment_id: int, session: orm.session.Session) -> datetime.datetime:
        return InvestmentCalcResult.unifyInvestmentResults(investment_id, session)

    @staticmethod
    def getLastFundResult(
        investment_id: int,
        fund_id: str,
        last_date: datetime.datetime,
        session: orm.session.Session
    ) -> None:
        try:
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
        except:
            logger.exception(
                "getLastFundResult(%s, %s, %s) failed to retrieve data from DB",
                investment_id,
                fund_id,
                last_date,
                exc_info=True
            )
            return None

    @staticmethod
    def unifyInvestmentResults(investment_id: int, session: orm.session.Session) -> datetime.datetime:

        logger.debug("unifyInvestmentResults(%s)", investment_id)

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
        logger.debug("Getting the last newest entry date")
        try:
            dateToFilter = (
                session
                .query(func.min(subquery.c.result_date))
                .filter(
                    subquery.c.rank == 1
                )
                .all()
            )[0][0]
        except:
            logger.exception("Failed to retrieve date from DB", exc_info=True)
            return None

        if dateToFilter == None:
            return None

        # Find rows with incomplete results and delete them
        # Example:
        # fund1 has last result from 02.01, but fund2 has result from 05.01,
        # query will delete all funds newer than 02.01,
        # which actually will be result with missing data from some funds
        logger.debug("Deleting the entries newer than %s", dateToFilter)
        try:
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
        except:
            logger.exception("Failed to delete DB entries", exc_info=True)

        # Return the edge date, before which the results are complete
        logger.debug("Returning filter date %s", dateToFilter)
        return dateToFilter
