"""
.DESCRIPTION
    class to check if connection to DB system can be established.
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      27-Mar-2024
    ChangeLog:

    Date            Who                     What

"""
from Utility.Logger import logger
import SQL
from SQL.read import Session_ro
from SQL.Fund import Fund


class SQLhealthCheck:

    @staticmethod
    def checkSQLConnection() -> bool:
        try:
            s_ro = Session_ro()
            s_ro.query(
                Fund
            ).all()
            s_ro.close()
            return True
        except:
            logger.exception("Failed to connect to DB", exc_info=True)
            return False
