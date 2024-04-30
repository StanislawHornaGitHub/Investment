"""
.DESCRIPTION
    Class definition for static methods related to configuring Investment moves
    selling or buying particular funds within Investment Wallet


.NOTES

    Version:            1.3
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      25-Mar-2024
    ChangeLog:

    Date            Who                     What
    2024-04-03      Stanisław Horna         Response body and code implemented.

    2024-04-26      Stanisław Horna         Method to retrieve investment funds with last refund date form db.
    
    2024-04-30      Stanisław Horna         Add logging capabilities.

"""
import json
import logging
import SQL
from SQL.Investment import Investment
from SQL.InvestmentResult import InvestmentResult

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from dateutil.parser import parse
from Utility.Dates import Dates


class InvestmentConfig:

    DateToStrFormat = "%Y-%m-%d"
    __default_date_for_none = "1900-01-01"

    @staticmethod
    def insertInvestmentConfig(Investments: dict[str, dict[str, list[dict[str, str]]]], InvestOwner: str):

        logging.debug("insertFundConfig()")
        # Create session and init processing variables
        session = SQL.base.Session()
        responseCode = 200
        result = []

        # Loop through each investment
        for invest in Investments:

            # Loop through each fund in investment
            for fund in Investments[invest]["Funds"]:
                logging.debug(
                    "Processing investment: %s, fund: %s", invest, fund
                )
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
                        responseCode = 400
                        logging.exception(
                            "Failed to create order entry, setting status code to: %d",
                            responseCode,
                            exc_info=True
                        )
                        result.append(
                            {
                                "Order Details": (
                                    f"{entry.investment_owner} - {entry.investment_fund_id} - {Dates.convertDateToString(entry.operation_quotation_date)} - {entry.operation_value}"
                                ),
                                "Status": "Failed to create order entry",
                                "Status_Details": str(err)
                            }
                        )

                        continue

                    logging.debug("Adding entry to session")
                    # Add new investment record
                    session.add(
                        entry
                    )
                    # Try to commit new entry
                    try:
                        session.commit()
                    except IntegrityError as err:
                        logging.warning(
                            "Current entry probably exists in DB",
                            exc_info=True
                        )
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
                        # Change responseCode to 206 (Partial Content), when investment order can not be added
                        # If there is set other code like 400 for some other orders, avoid changing it
                        if responseCode == 200:
                            responseCode = 206
                        logging.exception("Failed to add entry", exc_info=True)

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

        if responseCode == 200:
            result = {
                "Status": f"All {InvestOwner}'s {len(Investments)} investments inserted successfully"
            }

        session.close()

        logging.debug(
            "insertInvestmentConfig(). Returning body and code: %d",
            responseCode
        )
        return responseCode, result

    @staticmethod
    def importJSONconfig(filePath: str) -> dict[str, dict[str, any]]:
        with open(filePath, "r") as Invest:
            investments = json.loads(str("\n".join(Invest.readlines())))

        return investments

    @staticmethod
    def getInvestmentIDs(session):
        result = []
        try:
            output = (
                session
                .query(func.distinct(Investment.investment_id))
                .all()
            )
        except:
            logging.exception("Failed to get Investment IDs", exc_info=True)
            return None

        for id in output:
            result.append(id[0])
        return result

    @staticmethod
    def getInvestmentFunds(investment_id: int = None):

        logging.debug("getInvestmentFunds(%s)", investment_id)
        session = SQL.base.Session()
        responseCode = 200

        try:
            # Check if provided ID exists in DB
            if (
                (Investment.IDisValid(investment_id, session) != True) and
                (investment_id is not None)
            ):
                responseCode = 404
                logging.debug(
                    "Provided Investment ID %s does not exist, setting code to %d",
                    investment_id,
                    responseCode
                )
                resultBody = {
                    "Investment ID": investment_id,
                    "Status": f"Investment with ID: {investment_id} does not exist"
                }

                logging.debug(
                    "getInvestmentFunds(%s). Returning body and code: %d",
                    investment_id,
                    responseCode
                )
                return responseCode, resultBody

            if investment_id is not None:
                logging.debug("Investment ID is NOT none")
                dbOut = (
                    session.query(
                        Investment.investment_id,
                        Investment.investment_fund_id,
                        func.max(InvestmentResult.result_date)
                    ).outerjoin(
                        InvestmentResult,
                        (InvestmentResult.investment_id == Investment.investment_id) &
                        (InvestmentResult.fund_id == Investment.investment_fund_id)
                    ).group_by(
                        Investment.investment_id,
                        Investment.investment_fund_id
                    ).having(
                        Investment.investment_id == investment_id
                    ).all()
                )
            else:
                logging.debug("Investment ID is none")
                dbOut = (
                    session.query(
                        Investment.investment_id,
                        Investment.investment_fund_id,
                        func.max(InvestmentResult.result_date)
                    ).outerjoin(
                        InvestmentResult,
                        (InvestmentResult.investment_id == Investment.investment_id) &
                        (InvestmentResult.fund_id == Investment.investment_fund_id)
                    ).group_by(
                        Investment.investment_id,
                        Investment.investment_fund_id
                    )
                    .all()
                )
        except Exception as e:
            session.close()
            responseCode = 400
            logging.exception(
                "Failed to retrieve data from DB, setting status code to: %d",
                responseCode,
                exc_info=True
            )
            return responseCode, {
                "Status": "Failed to retrieve data from DB",
                "Status_Details": str(e)
            }
        session.close()

        logging.debug(
            "Converting DB output to list of dicts and datetime to str"
        )
        result = []
        for investmentID, fundID, investmentDate in dbOut:
            try:
                convertedDate = (
                    investmentDate.strftime(InvestmentConfig.DateToStrFormat)
                )
            except:
                convertedDate = InvestmentConfig.__default_date_for_none

            result.append(
                {
                    "investment_id": investmentID,
                    "fund_id": fundID,
                    "refund_date": convertedDate
                }
            )

        logging.debug(
            "getInvestmentFunds(%s). Returning body and code: %d",
            investment_id,
            responseCode
        )
        return responseCode, result
