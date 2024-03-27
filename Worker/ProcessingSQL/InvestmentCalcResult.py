
import SQL
from SQL.Quotation import Quotation
from SQL.InvestmentResult import InvestmentResult
from SQL.Investment import Investment
from sqlalchemy import func

from sqlalchemy.exc import DatabaseError
import datetime

from Worker.Utility import DebugOutput

class InvestmentCalcResult:

    @staticmethod
    def calculateResult(investment_id: int):
        session = SQL.base.Session()
        start_date, funds, ordersMap = InvestmentCalcResult.getInvestmentOrderMap(
            investment_id, session
        )
        quot = InvestmentCalcResult.getFundsQuotation(
            funds, start_date, session
        )
        lastUpdateDate = InvestmentCalcResult.getLastResultDate(
            investment_id, session
        )
        tempOwnedFunds = {}
        if lastUpdateDate == None:
            currentProcessingDate = start_date
            
            for fund in funds:
                tempOwnedFunds[fund] = {
                    "ParticipationUnits": 0,
                    "InvestedMoney": 0
                }
        else:
            for fund in funds:
                LastFundResult = InvestmentCalcResult.getLastFundResult(fund,lastUpdateDate,session)
                tempOwnedFunds[fund] = {
                    "ParticipationUnits": LastFundResult[0],
                    "InvestedMoney": LastFundResult[0]
                }
            currentProcessingDate = (lastUpdateDate + datetime.timedelta(days=1))
        
        result = []

        while ((currentProcessingDate <= datetime.datetime.now())):

            if currentProcessingDate in list(ordersMap.keys()):
                for fund in ordersMap[currentProcessingDate]:

                    tempOwnedFunds[fund]["ParticipationUnits"] += (
                        ordersMap[currentProcessingDate][fund]["Money"] /
                        quot[fund][currentProcessingDate]
                    )
                    tempOwnedFunds[fund]["InvestedMoney"] += (
                        ordersMap[currentProcessingDate][fund]["Money"]
                    )

            for fund in funds:
                try:
                    result.append(
                        {
                            "result_date": currentProcessingDate,
                            "investment_id": investment_id,
                            "fund_id": fund,
                            "fund_participation_units": (
                                tempOwnedFunds[fund]["ParticipationUnits"]
                            ),
                            "fund_invested_money":(
                                tempOwnedFunds[fund]["InvestedMoney"]
                            ),
                            "fund_value":(
                                tempOwnedFunds[fund]["ParticipationUnits"] *
                                quot[fund][currentProcessingDate]
                            )
                        }
                    )
                except:
                    #print("Missing date: ", currentProcessingDate)
                    pass

            currentProcessingDate += datetime.timedelta(days=1)

        DebugOutput.CSV_writer.saveFile(result,f"invest_{investment_id}.csv")
        
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
            .query(InvestmentResult.fund_participation_units,InvestmentResult.fund_invested_money)
            .filter(InvestmentResult.fund_id == fund_id, InvestmentResult.result_date == last_date)
            .first()
        )