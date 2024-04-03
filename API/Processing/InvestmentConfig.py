"""
.DESCRIPTION
    Class definition for static methods related to configuring Investment moves
    selling or buying particular funds within Investment Wallet
    

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      25-Mar-2024
    ChangeLog:

    Date            Who                     What
    2024-04-03      Stanisław Horna         Response body and code implemented.

"""
import json
import SQL
from SQL.Investment import Investment

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from dateutil.parser import parse
from Utility.Dates import Dates


class InvestmentConfig:

    @staticmethod
    def insertInvestmentConfig(Investments: dict[str, dict[str, list[dict[str, str]]]], InvestOwner: str):

        # Create session and init processing variables
        session = SQL.base.Session()
        responseCode = 200
        result = []

        # Loop through each investment
        for invest in Investments:

            # Loop through each fund in investment
            for fund in Investments[invest]["Funds"]:

                # Loop through each order in investment
                for i in range(len(Investments[invest]["Funds"][fund])):

                    # Try to create investment order record

                    try:
                        entry = Investment(
                            investment_id=None,
                            investment_name=invest,
                            investment_owner_id=None,
                            investment_owner=InvestOwner,
                            investment_fund_id=fund,
                            operation_quotation_date=parse(
                                Investments[invest]["Funds"][fund][i]["BuyDate"]
                            ),
                            operation_value=Investments[invest]["Funds"][fund][i]["Money"]
                        )
                    except Exception as err:
                        result.append(
                            {
                                "Order Details": (
                                    f"{entry.investment_owner} - {entry.investment_fund_id} - {Dates.convertDateToString(entry.operation_quotation_date)} - {entry.operation_value}"
                                ),
                                "Status": "Failed to create order entry",
                                "Status_Details": str(err)
                            }
                        )
                        responseCode = 400
                        continue

                    # Add new investment record
                    session.add(
                        entry
                    )
                    # Try to commit new entry
                    try:
                        session.commit()
                    except IntegrityError as err:
                        
                        # Rollback transaction to be able to successfully proceed with order
                        session.rollback()

                        # Extract error
                        errorMessage = (
                            " - ".join(
                                [phrase for phrase in str(err).split('\n')
                                 if ("DETAIL: " in phrase) or ("(psycopg2.errors." in phrase)]
                            )
                        )
                        
                        # Append result variable with details
                        result.append(
                            {
                                "Order Details": (
                                    f"{entry.investment_owner} - {entry.investment_fund_id} - {Dates.convertDateToString(entry.operation_quotation_date)} - {entry.operation_value}"
                                ),
                                "Status": "Already exists",
                                "Status_Details": errorMessage
                            }
                        )
                        
                    except Exception as e:
                        
                        # Rollback transaction to be able to successfully proceed with order
                        session.rollback()
                        
                        # Add error message without further analysis
                        result.append(
                            {
                                "Order Details": (
                                    f"{entry.investment_owner} - {entry.investment_fund_id} - {Dates.convertDateToString(entry.operation_quotation_date)} - {entry.operation_value}"
                                ),
                                "Status": "Failed to add",
                                "Status_Details": str(e)
                            }
                        )
                        
                        # Change responseCode to 206 (Partial Content), when investment order can not be added
                        # If there is set other code like 400 for some other orders, avoid changing it
                        if responseCode == 200:
                            responseCode = 206
                        
        if responseCode == 200:
            result = {
                "Status": f"All {InvestOwner}'s {len(Investments)} investments inserted successfully"
            }
        
        session.close()

        return responseCode, result

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
