"""
.DESCRIPTION
    Class definition for static methods related to monitored funds configuration.
    

.NOTES

    Version:            1.3
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      27-Mar-2024
    ChangeLog:

    Date            Who                     What
    2024-04-02      Stanisław Horna         Response body and code implemented.
    
    2024-04-26      Stanisław Horna         Method to retrieve monitored funds with last quotation date form db.
    
    2024-04-30      Stanisław Horna         Add logging capabilities.

"""
import json
import logging
import SQL
from sqlalchemy import func
from SQL.Fund import Fund
from SQL.Quotation import Quotation
from sqlalchemy.exc import IntegrityError


class FundConfig:

    DateToStrFormat = "%Y-%m-%d"
    __default_date_for_none = "1900-01-01"

    @staticmethod
    def insertFundConfig(Funds: list[str]):

        logging.debug("insertFundConfig()")
        # Create session and init processing variables
        session = SQL.base.Session()
        responseCode = 200
        result = []

        # Loop through provided URLs
        for url in Funds:

            logging.debug("Processing: %s", url)

            # Try to create entry for current URL
            try:
                entry = Fund(url)
                session.add(entry)
                session.commit()

            # Catch Integrity errors i.e. fund id already exists
            except IntegrityError as err:

                logging.warning(
                    "Current entry probably exists in DB",
                    exc_info=True
                )

                # Rollback transaction to be able to successfully proceed with the next url
                session.rollback()

                # Extract error
                errorMessage = " - ".join([phrase for phrase in str(err).split(
                    '\n') if ("DETAIL: " in phrase) or ("(psycopg2.errors." in phrase)])

                result.append(
                    {
                        "Fund_ID": entry.fund_id,
                        "Fund_URL": entry.fund_url,
                        "Status": "Already exists",
                        "Status_Details": errorMessage
                    }
                )

                # Change responseCode to 206 (Partial Content), when only fund can not be processed
                # If there is set other code like 400 for some other url, avoid changing it
                if responseCode == 200:
                    responseCode = 206

                # Go to next iteration
                continue

            except Exception as e:
                responseCode = 400
                logging.exception(
                    "Exception occurred, setting code to: %d",
                    responseCode,
                    exc_info=True
                )
                # Rollback transaction to be able to successfully proceed with the next url
                session.rollback()

                # Add error message without further analysis
                result.append(
                    {
                        "Fund_ID": entry.fund_id,
                        "Fund_URL": entry.fund_url,
                        "Status": "Failed to add",
                        "Status_Details": str(e)
                    }
                )

        # Set message if all funds were inserted successfully
        if responseCode == 200:
            logging.info("All %d fund URLs inserted successfully", len(Funds))
            result = {
                "Status": f"All {len(Funds)} fund URLs inserted successfully"
            }

        # Close SQL session
        session.close()
        logging.debug(
            "insertFundConfig(). Returning body and code: %d",
            responseCode
        )
        return responseCode, result

    @staticmethod
    def importJSONconfig(filePath: str) -> list[str]:
        with open(filePath, "r") as Invest:
            investments = json.loads(str("\n".join(Invest.readlines())))

        return investments["FundsToCheckURLs"]

    @staticmethod
    def getFund(fund_id: str = None) -> list[dict[str, str]]:

        logging.debug("getFund(%s)", fund_id)

        session = SQL.base.Session()
        responseCode = 200
        try:
            if fund_id is not None:
                logging.debug("fund ID is NOT none")
                dbOut = (
                    session.query(
                        Quotation.fund_id,
                        Fund.category_short,
                        func.max(Quotation.date)
                    ).outerjoin(
                        Fund,
                        Fund.fund_id == Quotation.fund_id
                    ).filter(
                        Fund.fund_id == fund_id
                    ).group_by(
                        Quotation.fund_id,
                        Fund.category_short
                    )
                    .all()
                )
            else:
                logging.debug("fund ID is none")
                dbOut = (
                    session.query(
                        Quotation.fund_id,
                        Fund.category_short,
                        func.max(Quotation.date)
                    ).outerjoin(
                        Fund,
                        Fund.fund_id == Quotation.fund_id
                    ).group_by(
                        Quotation.fund_id,
                        Fund.category_short
                    )
                    .all()
                )
        except Exception as e:
            session.close()
            responseCode = 400
            logging.exception(
                "getFund(%s) failed to retrieve data from DB, setting status code to: %d",
                fund_id,
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
        for fundID, fundCat, fundDate in dbOut:
            try:
                convertedDate = fundDate.strftime(FundConfig.DateToStrFormat)
            except:
                convertedDate = FundConfig.__default_date_for_none

            result.append(
                {
                    "fund_id": fundID,
                    "fund_category": fundCat,
                    "quotation_date": convertedDate
                }
            )
        logging.debug(
            "getFund(%s). Returning body and code: %d",
            fund_id,
            responseCode
        )
        return responseCode, result
