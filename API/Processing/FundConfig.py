"""
.DESCRIPTION
    Class definition for static methods related to monitored funds configuration.
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      27-Mar-2024
    ChangeLog:

    Date            Who                     What

"""
import json

import SQL
from SQL.Fund import Fund
from sqlalchemy.exc import DatabaseError


class FundConfig:
    
    @staticmethod
    def insertFundConfig(Funds: list[str]):
        session = SQL.base.Session()
        for url in Funds:
            try:
                entry = Fund(url)
                session.add(entry)
                session.commit()
            except DatabaseError as err:
                session.rollback()
                print(" - ".join([phrase for phrase in str(err).split('\n') if ("DETAIL: " in phrase) or ("(psycopg2.errors." in phrase)]))
                continue
            except: 
                pass
                
                
        session.close()
        
        return None

    @staticmethod
    def importJSONconfig(filePath: str) -> list[str]:
        with open(filePath, "r") as Invest:
            investments = json.loads(str("\n".join(Invest.readlines())))
        
        return investments["FundsToCheckURLs"]
    
