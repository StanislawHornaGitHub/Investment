"""
.DESCRIPTION
    Class definition for static methods related downloading fund quotation from the Internet.

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      24-Mar-2024
    ChangeLog:

    Date            Who                     What

"""
import SQL
from SQL.Quotation import Quotation
from SQL.Fund import Fund
from AnalizyPL.API import AnalizyFund
from Utility.ConvertToDict import ConvertToDict
from sqlalchemy import func

from Utility.Dates import Dates


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
            allQuotations = downloadedQuot["FundQuotation"]
            downloadedQuot["FundQuotation"] = [
                q for q in downloadedQuot["FundQuotation"] 
                if q[AnalizyFund.RESPONSE_DATE_NAME]>date
                ]
            
            Price.insertRecord_Q(downloadedQuot, session, allQuotations)
        
        fundsWithPrice = list([fr[1] for fr in lastRefreshDates])
        fundsWithoutPrice = [
            f for f in list(fund.keys()) 
            if f not in fundsWithPrice
            ]
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
    def insertRecord_Q(dataToInsert: list[dict[str, str]], session, allQuotation = []):
        
        for entry in dataToInsert["FundQuotation"]:
            
            currentDate = entry[AnalizyFund.RESPONSE_DATE_NAME]
            currentValue = entry[AnalizyFund.RESPONSE_PRICE_NAME]
            
            result = {
                'daily': None,
                'weekly': None,
                'monthly': None,
                'yearly': None
            }
            
            dates = Dates.getDesiredDates(currentDate)
            
            for period in dates:
                if (prev_value := Dates.getEntryWithDesiredDate(
                    allQuotation + dataToInsert["FundQuotation"],
                    AnalizyFund.RESPONSE_DATE_NAME,
                    dates[period]
                )
                    ) != None:
                    result[period] = (currentValue / prev_value[AnalizyFund.RESPONSE_PRICE_NAME]) - 1.0
            
            
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
        