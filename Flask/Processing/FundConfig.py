"""
.DESCRIPTION
    Class definition for static methods related to monitored funds configuration.
    

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      27-Mar-2024
    ChangeLog:

    Date            Who                     What
    2024-04-02      Stanisław Horna         Response body and code implemented.
    
    2024-04-26      Stanisław Horna         Method to retrieve monitored funds with last quotation date form db.

"""
import json

import SQL
from sqlalchemy import func
from SQL.Fund import Fund
from SQL.Quotation import Quotation
from sqlalchemy.exc import IntegrityError


class FundConfig:
    
    DateToStrFormat = "%Y-%m-%d"

    @staticmethod
    def insertFundConfig(Funds: list[str]):

        # Create session and init processing variables
        session = SQL.base.Session()
        responseCode = 200
        result = []

        # Loop through provided URLs
        for url in Funds:

            # Try to create entry for current URL
            try:
                entry = Fund(url)
                session.add(entry)
                session.commit()

            # Catch Integrity errors i.e. fund id already exists
            except IntegrityError as err:

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
                print(errorMessage)

                # Change responseCode to 206 (Partial Content), when only fund can not be processed
                # If there is set other code like 400 for some other url, avoid changing it
                if responseCode == 200:
                    responseCode = 206

                # Go to next iteration
                continue

            except Exception as e:
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
                responseCode = 400

        # Set message if all funds were inserted successfully
        if responseCode == 200:
            result = {
                "Status": f"All {len(Funds)} fund URLs inserted successfully"
            }

        # Close SQL session
        session.close()

        return responseCode, result

    @staticmethod
    def importJSONconfig(filePath: str) -> list[str]:
        with open(filePath, "r") as Invest:
            investments = json.loads(str("\n".join(Invest.readlines())))

        return investments["FundsToCheckURLs"]

    @staticmethod
    def getFundUrls() -> list[dict[str, str]]:
        
        session = SQL.base.Session()
        responseCode = 200
        try:
            dbOut = (
                session.query(
                    Quotation.fund_id,
                    Fund.fund_url,
                    func.max(Quotation.date)
                ).outerjoin(
                    Fund,
                    Fund.fund_id == Quotation.fund_id
                ).group_by(
                    Quotation.fund_id,
                    Fund.fund_url
                )
                .all()
            )
        except Exception as e:
            responseCode = 400
            return responseCode, {
                "Status": "Failed to retrieve data from DB",
                "Status_Details": str(e)
            }
        result = []
        for fundID, fundURL, fundDate in dbOut:
            result.append(
                {
                    "fund_id": fundID,
                    "fund_url": fundURL,
                    "quotation_date": fundDate.strftime(FundConfig.DateToStrFormat)
                }
            )
        
        return responseCode, result
