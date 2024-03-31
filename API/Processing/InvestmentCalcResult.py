
import SQL
from SQL.Quotation import Quotation
from SQL.InvestmentResult import InvestmentResult
from SQL.Investment import Investment
from sqlalchemy import func

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
        
        # Create new SQL session
        session = SQL.base.Session()

        # Get IDs for investments existing in DB
        investmentsToRefresh = InvestmentConfig.getInvestmentIDs(session)

        # Loop through each investment and invoke result calculation
        for id in investmentsToRefresh:
            InvestmentCalcResult.calculateResult(id)
        
        # Close SQL session
        session.close()
        
        return None

    @staticmethod
    def calculateResult(investment_id: int):
        
        # Create new SQL session
        session = SQL.base.Session()
        
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
                    fund, lastUpdateDate, session)
                
                tempOwnedFunds[fund] = {
                    "ParticipationUnits": LastFundResult[0],
                    "InvestedMoney": LastFundResult[1]
                }
            
            # Increment processing date to the next date as
            # lastUpdateDate is a date retrieved form DB, which means it was already calculated
            currentProcessingDate = Dates.addDays(lastUpdateDate, 1)
            
            # Get historical data to be able to calculate profits compared to last week, month etc.
            SQLdata = InvestmentResult.getInvestmentResult(investment_id, session)

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
                        colName = InvestmentCalcResult.ConvertPeriodNamesDatesToInvestmentResult[date]
                        
                        # and try to calculate the result.
                        # try is required as used method can create entries with 0,
                        # for funds which were not bought since the beginning of investment
                        try:
                            record[colName] = (
                                (
                                    (record["fund_value"] - record["fund_invested_money"]) - 
                                    (entryToCompare["fund_value"] - entryToCompare["fund_invested_money"])
                                ) 
                            )
                        except:
                            # If calculation fails, nothing to worry, fund was not bought yet.
                            pass
                
                # Append the result list with entry ready to insert to DB
                result.append(record)

            # Calculate next processing date and go to the beginning of while loop
            currentProcessingDate = Dates.addDays(currentProcessingDate, 1)

        # Loop through each entry in result var, create an DB entry, add it to session and try to commit.
        for output in result:
            record = InvestmentResult(
                **output
            )
            session.add(record)
            try:
                session.commit()
            except DatabaseError as err:
                session.rollback()
                print(err)
                print(output)
        
        return None

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
        return (
            session
            .query(func.max(InvestmentResult.result_date))
            .filter(InvestmentResult.investment_id == investment_id)
            .first()
        )[0]

    @staticmethod
    def getLastFundResult(fund_id: str, last_date, session):
        return (
            session
            .query(InvestmentResult.fund_participation_units, InvestmentResult.fund_invested_money)
            .filter(InvestmentResult.fund_id == fund_id, InvestmentResult.result_date == last_date)
            .first()
        )
