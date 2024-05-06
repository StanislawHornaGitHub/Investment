"""
.DESCRIPTION
    Class definition for static methods related to configuring Investment moves
    selling or buying particular funds within Investment Wallet


.NOTES

    Version:            1.4
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      25-Mar-2024
    ChangeLog:

    Date            Who                     What
    2024-04-03      Stanisław Horna         Response body and code implemented.

    2024-04-26      Stanisław Horna         Method to retrieve investment funds with last refund date form db.
    
    2024-04-30      Stanisław Horna         Add logging capabilities.

    2024-05-06      Stanisław Horna         Add missing I/O datatypes. Refactor variable names.

"""

import json
from sqlalchemy import func, orm
from sqlalchemy.exc import IntegrityError
from dateutil.parser import parse
from SQL.Investment import Investment
from SQL.InvestmentResult import InvestmentResult
from SQL.write import Session_rw
from SQL.read import Session_ro
from Utility.Dates import Dates
from Utility.Logger import logger


class InvestmentConfig:

    DateToStrFormat = "%Y-%m-%d"
    __default_date_for_none = "1900-01-01"

    @staticmethod
    def insertInvestmentConfig(
        Investments: dict[str, dict[str, list[dict[str, str]]]],
        InvestOwner: str
    ) -> tuple[int, list[dict[str, str]]]:

        logger.debug("insertFundConfig()")
        # Create session and init processing variables
        s_rw = Session_rw()
        responseCode = 200
        responseBody = []

        # Loop through each investment
        for invest in Investments:

            # Loop through each fund in investment
            for fund in Investments[invest]["Funds"]:
                logger.debug(
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
                        logger.exception(
                            "Failed to create order entry, setting status code to: %d",
                            responseCode,
                            exc_info=True
                        )
                        responseBody.append(
                            {
                                "Order Details": (
                                    f"{entry.investment_owner} - {entry.investment_fund_id} - {Dates.convertDateToString(entry.operation_quotation_date)} - {entry.operation_value}"
                                ),
                                "Status": "Failed to create order entry",
                                "Status_Details": str(err)
                            }
                        )

                        continue

                    logger.debug("Adding entry to session")
                    # Add new investment record
                    s_rw.add(
                        entry
                    )
                    # Try to commit new entry
                    try:
                        s_rw.commit()
                    except IntegrityError as err:
                        logger.warning(
                            "Current entry probably exists in DB",
                            exc_info=True
                        )
                        # Rollback transaction to be able to successfully proceed with order
                        s_rw.rollback()

                        # Extract error
                        errorMessage = (
                            " - ".join(
                                [phrase for phrase in str(err).split('\n')
                                 if ("DETAIL: " in phrase) or ("(psycopg2.errors." in phrase)]
                            )
                        )

                        # Append responseBody variable with details
                        responseBody.append(
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
                        logger.exception("Failed to add entry", exc_info=True)

                        # Rollback transaction to be able to successfully proceed with order
                        s_rw.rollback()

                        # Add error message without further analysis
                        responseBody.append(
                            {
                                "Order Details": (
                                    f"{entry.investment_owner} - {entry.investment_fund_id} - {Dates.convertDateToString(entry.operation_quotation_date)} - {entry.operation_value}"
                                ),
                                "Status": "Failed to add",
                                "Status_Details": str(e)
                            }
                        )

        if responseCode == 200:
            responseBody = {
                "Status": f"All {InvestOwner}'s {len(Investments)} investments inserted successfully"
            }

        s_rw.close()

        logger.debug(
            "insertInvestmentConfig(). Returning body and code: %d",
            responseCode
        )
        return responseCode, responseBody

    @staticmethod
    def importJSONconfig(filePath: str) -> dict[str, dict[str, any]]:
        with open(filePath, "r") as Invest:
            investments = json.loads(str("\n".join(Invest.readlines())))

        return investments

    @staticmethod
    def getInvestmentIDs(session: orm.session.Session) -> list[int]:
        result = []
        try:
            output = (
                session
                .query(func.distinct(Investment.investment_id))
                .all()
            )
        except:
            logger.exception("Failed to get Investment IDs", exc_info=True)
            return None

        for id in output:
            result.append(id[0])
        return result

    @staticmethod
    def getInvestmentFunds(investment_id: int = None) -> tuple[int, list[dict[str, str]]]:

        logger.debug("getInvestmentFunds(%s)", investment_id)
        s_ro = Session_ro()
        responseCode = 200

        try:
            # Check if provided ID exists in DB
            if (
                (Investment.IDisValid(investment_id, s_ro) != True) and
                (investment_id is not None)
            ):
                responseCode = 404
                logger.debug(
                    "Provided Investment ID %s does not exist, setting code to %d",
                    investment_id,
                    responseCode
                )
                responseBody = {
                    "Investment ID": investment_id,
                    "Status": f"Investment with ID: {investment_id} does not exist"
                }

                logger.debug(
                    "getInvestmentFunds(%s). Returning body and code: %d",
                    investment_id,
                    responseCode
                )
                return responseCode, responseBody

            if investment_id is not None:
                logger.debug("Investment ID is NOT none")
                dbOut = (
                    s_ro.query(
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
                logger.debug("Investment ID is none")
                dbOut = (
                    s_ro.query(
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
            s_ro.close()
            responseCode = 400
            logger.exception(
                "Failed to retrieve data from DB, setting status code to: %d",
                responseCode,
                exc_info=True
            )
            return responseCode, {
                "Status": "Failed to retrieve data from DB",
                "Status_Details": str(e)
            }
        s_ro.close()

        logger.debug(
            "Converting DB output to list of dicts and datetime to str"
        )
        responseBody = []
        for investmentID, fundID, investmentDate in dbOut:
            try:
                convertedDate = (
                    investmentDate.strftime(InvestmentConfig.DateToStrFormat)
                )
            except:
                convertedDate = InvestmentConfig.__default_date_for_none

            responseBody.append(
                {
                    "investment_id": investmentID,
                    "fund_id": fundID,
                    "refund_date": convertedDate
                }
            )

        logger.debug(
            "getInvestmentFunds(%s). Returning body and code: %d",
            investment_id,
            responseCode
        )
        return responseCode, responseBody
