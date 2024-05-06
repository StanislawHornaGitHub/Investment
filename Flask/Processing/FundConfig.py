"""
.DESCRIPTION
    Class definition for static methods related to monitored funds configuration.
    

.NOTES

    Version:            1.5
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      27-Mar-2024
    ChangeLog:

    Date            Who                     What
    2024-04-02      Stanisław Horna         Response body and code implemented.
    
    2024-04-26      Stanisław Horna         Method to retrieve monitored funds with last quotation date form db.
    
    2024-04-30      Stanisław Horna         Add logging capabilities.
    
    2024-05-04      Stanisław Horna         Remove status details and fund url from body response in insertFundConfig()

    2024-05-06      Stanisław Horna         Add missing I/O datatypes. Refactor variable names.

"""

import json
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from SQL.Fund import Fund
from SQL.Quotation import Quotation
from SQL.write import Session_rw
from SQL.read import Session_ro
from Utility.Logger import logger


class FundConfig:

    DateToStrFormat = "%Y-%m-%d"
    __default_date_for_none = "1900-01-01"

    @staticmethod
    def insertFundConfig(Funds: list[str]) -> tuple[int, list[dict[str, str]]]:

        logger.debug("insertFundConfig()")
        # Create session and init processing variables
        s_rw = Session_rw()
        responseCode = 200
        responseBody = []

        # Loop through provided URLs
        for url in Funds:

            logger.debug("Processing: %s", url)

            # Try to create entry for current URL
            try:
                entry = Fund(url)
                s_rw.add(entry)
                s_rw.commit()

            # Catch Integrity errors i.e. fund id already exists
            except IntegrityError as err:

                logger.warning(
                    "Current entry probably exists in DB",
                    exc_info=True
                )

                # Rollback transaction to be able to successfully proceed with the next url
                s_rw.rollback()

                responseBody.append(
                    {
                        "Fund_ID": entry.fund_id,
                        "Status": "Already exists",
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
                logger.exception(
                    "Exception occurred, setting code to: %d",
                    responseCode,
                    exc_info=True
                )
                # Rollback transaction to be able to successfully proceed with the next url
                s_rw.rollback()

                # Add error message without further analysis
                responseBody.append(
                    {
                        "Fund_ID": entry.fund_id,
                        "Status": "Failed to add",
                    }
                )

        # Set message if all funds were inserted successfully
        if responseCode == 200:
            logger.info("All %d fund URLs inserted successfully", len(Funds))
            responseBody = {
                "Status": f"All {len(Funds)} fund URLs inserted successfully"
            }

        # Close SQL session
        s_rw.close()
        logger.debug(
            "insertFundConfig(). Returning body and code: %d",
            responseCode
        )
        return responseCode, responseBody

    @staticmethod
    def importJSONconfig(filePath: str) -> list[str]:
        with open(filePath, "r") as Invest:
            investments = json.loads(str("\n".join(Invest.readlines())))

        return investments["FundsToCheckURLs"]

    @staticmethod
    def getFund(fund_id: str = None) -> tuple[int, list[dict[str, str]]]:

        logger.debug("getFund(%s)", fund_id)

        s_ro = Session_ro()
        responseCode = 200
        try:
            # If fund id is not provided return latest quotation date for each fund
            if fund_id is not None:
                logger.debug("fund ID is NOT none")
                dbOut = (
                    s_ro.query(
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
                # If fund id is provided return latest quotation date for selected fund
                logger.debug("fund ID is none")
                dbOut = (
                    s_ro.query(
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
            s_ro.close()
            responseCode = 400
            logger.exception(
                "getFund(%s) failed to retrieve data from DB, setting status code to: %d",
                fund_id,
                responseCode,
                exc_info=True
            )
            return responseCode, {
                "Status": "Failed to retrieve data from DB",
            }
        s_ro.close()
        logger.debug(
            "Converting DB output to list of dicts and datetime to str"
        )
        responseBody = []
        for fundID, fundCat, fundDate in dbOut:
            try:
                convertedDate = fundDate.strftime(FundConfig.DateToStrFormat)
            except:
                convertedDate = FundConfig.__default_date_for_none

            responseBody.append(
                {
                    "fund_id": fundID,
                    "fund_category": fundCat,
                    "quotation_date": convertedDate
                }
            )
        logger.debug(
            "getFund(%s). Returning body and code: %d",
            fund_id,
            responseCode
        )
        return responseCode, responseBody
