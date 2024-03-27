import SQL
from SQL.Quotation import Quotation
from SQL.Fund import Fund
from AnalizyPL.API import AnalizyFund
from Worker.Utility.ConvertToDict import ConvertToDict
from sqlalchemy import func

from dateutil.parser import parse
import datetime

class Price:

    @staticmethod
    def updateQuotation():
        session = SQL.base.Session()
        fund = ConvertToDict.fundList(session.query(Fund).all())
        lastRefreshDates = (session
                            .query(func.max(Quotation.date), Quotation.fund_id)
                            .group_by(Quotation.fund_id)
                            .all()
                            )
        for date, fundID in lastRefreshDates:
            downloadedQuot = AnalizyFund.downloadQuotation(fund[fundID])
            downloadedQuot["FundQuotation"] = [
                q for q in downloadedQuot["FundQuotation"] 
                if parse(q[AnalizyFund.RESPONSE_DATE_NAME])>date
                ]
            
            Price.insertRecord_Q(downloadedQuot, session)
        
        fundsWithPrice = list([fr[1] for fr in lastRefreshDates])
        fundsWithoutPrice = [
            f for f in list(fund.keys()) 
            if f not in fundsWithPrice
            ]
        print(fundsWithoutPrice)
        Price.insertQuotation(fundsWithoutPrice, fund, session)

        session.commit()
        session.close()
        return None
    
    @staticmethod
    def insertQuotation(fundsWithoutPrice: list[str], allFunds: dict[str, Fund], session):
        for fundID in fundsWithoutPrice:
            downloadedQuot = AnalizyFund.downloadQuotation(allFunds[fundID])
            Price.insertRecord_Q(downloadedQuot, session)

        return None
    

    @staticmethod
    def insertRecord_Q(dataToInsert: list[dict[str, str]], session):
        
        fundID = dataToInsert["Fund_ID"]
        
        for entry in dataToInsert["FundQuotation"]:
            
            currentDate = parse(entry[AnalizyFund.RESPONSE_DATE_NAME])
            currentValue = float(entry[AnalizyFund.RESPONSE_PRICE_NAME])
            
            result = {
                'daily': None,
                'weekly': None,
                'monthly': None,
                'yearly': None
            }
            
            dates = Price.getDesiredDates(currentDate)
            
            for period in dates:
                if (prev_value := Price.getHistoricalQuotation(
                        dates[period],
                        fundID, 
                        session
                        )
                    ) != None:
                    result[period] = (currentValue / prev_value[0]) - 1.0
            
            
            session.add(
                Quotation(
                    currentDate,
                    dataToInsert["Fund_ID"],
                    currentValue,
                    result["daily"],
                    result["weekly"],
                    result["monthly"],
                    result["yearly"],
                )
            )
        session.commit()

        
        
    @staticmethod
    def getHistoricalQuotation(desired_date, fund_id, session):
        
        return (
            session
            .query(Quotation.value)
            .filter(Quotation.date < desired_date, Quotation.fund_id == fund_id)
            .order_by(Quotation.date.desc())
            .limit(1)
            .first()
        )
        
    @staticmethod
    def getDesiredDates(currentDate: datetime) -> dict[str, datetime.datetime]:
        return {
            'daily': (currentDate - datetime.timedelta(
                days=1
            )),
            'weekly': (currentDate - datetime.timedelta(
                days=7
            )),
            'monthly': (currentDate - datetime.timedelta(
                days=30
            )),
            'yearly': (currentDate - datetime.timedelta(
                days=365
            )),
        }