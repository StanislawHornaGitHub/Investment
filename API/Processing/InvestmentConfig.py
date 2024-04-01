"""
.DESCRIPTION
    Class definition for static methods related to configuring Investment moves
    selling or buying particular funds within Investment Wallet
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      25-Mar-2024
    ChangeLog:

    Date            Who                     What

"""
import json
import SQL
from SQL.Investment import Investment

from sqlalchemy import func
from sqlalchemy.exc import DatabaseError
from dateutil.parser import parse
import datetime


class InvestmentConfig:
    
    @staticmethod
    def insertInvestmentConfig(Investments: dict[str, dict[str, list[dict[str, str]]]], InvestOwner: str):
        session = SQL.base.Session()
        for invest in Investments:
            for fund in Investments[invest]["Funds"]:
                for i in range(len(Investments[invest]["Funds"][fund])):
                    session.add(
                        Investment(
                            investment_id=None,
                            investment_name=invest,
                            investment_owner_id=None,
                            investment_owner=InvestOwner,
                            investment_fund_id=fund,
                            operation_quotation_date=parse(Investments[invest]["Funds"][fund][i]["BuyDate"]),
                            operation_value=Investments[invest]["Funds"][fund][i]["Money"]
                        )
                    )
                    try:
                        session.commit()
                    except DatabaseError as err:
                        session.rollback()
                        print(" - ".join([phrase for phrase in str(err).split('\n') if ("DETAIL: " in phrase) or ("(psycopg2.errors." in phrase)]))
        session.close()
        
        return None

    @staticmethod
    def importJSONconfig(filePath: str) -> dict[str, dict[str, any]]:
        with open(filePath, "r") as Invest:
            investments = json.loads(str("\n".join(Invest.readlines())))
        
        return investments
    
    @staticmethod
    def getInvestmentIDs(session):
        result = []
        output = (
            session
            .query(func.distinct(Investment.investment_id))
            .all()
        )
        for id in output:
            result.append(id[0])
        return result