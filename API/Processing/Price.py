"""
.DESCRIPTION
    Class definition for static methods related downloading fund quotation from the Internet.

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      24-Mar-2024
    ChangeLog:

    Date            Who                     What
    2024-04-02      Stanisław Horna         Response body and code implemented.

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

        # Create session and init processing variables
        session = SQL.base.Session()
        responseCode = 200
        result = []

        # Get monitored Fund IDs
        fund = ConvertToDict.fundList(session.query(Fund).all())

        # Get last quotation date for each fund
        lastRefreshDates = (
            session
            .query(func.max(Quotation.date), Quotation.fund_id)
            .group_by(Quotation.fund_id)
            .all()
        )

        # Loop through each fund which already has some quotation in DB
        for date, fundID in lastRefreshDates:

            try:
                # Download newest quotation from Analizy.pl
                downloadedQuot = AnalizyFund.downloadQuotation(fund[fundID])
            except Exception as err:
                responseCode = 204
                result.append(
                    {
                        "Fund ID": fundID,
                        "Status": "Failed to download quotation",
                        "Status Details": str(err)
                    }
                )
                continue

            # Create temp variable to store all downloaded quotation
            allQuotations = downloadedQuot["FundQuotation"]

            # Filter out the quotation to only those entries which will be inserted to DB
            downloadedQuot["FundQuotation"] = [
                q for q in downloadedQuot["FundQuotation"]
                if q[AnalizyFund.RESPONSE_DATE_NAME] > date
            ]

            # Insert quotation to DB
            code, responseBody = Price.insertQuotationRecords(
                downloadedQuot,
                session,
                allQuotations
            )

            responseBody["Fund ID"] = fundID

            result.append(responseBody)

            if code != 204:
                responseCode = code

        # Get funds without any quotation
        fundsWithPrice = list([fr[1] for fr in lastRefreshDates])
        fundsWithoutPrice = [
            f for f in list(fund.keys())
            if f not in fundsWithPrice
        ]

        # Download and insert all available quotation for funds without them
        insertStatus = Price.insertQuotation(fundsWithoutPrice, fund, session)

        # Extract error codes from .insertQuotation() method output
        errorCodes = [entry["responseCode"] for entry in insertStatus]

        # Append existing response code with those from .insertQuotation() method
        if responseCode != 204:
            if 206 in errorCodes:
                responseCode = 206

            if 204 in errorCodes:
                responseCode = 204

        # Append all error entries form .insertQuotation() method
        for entry in insertStatus:
            result.append(entry["responseBody"])

        # Close SQL session
        session.close()

        return responseCode, result

    @staticmethod
    def insertQuotation(fundsWithoutPrice: list[str], allFunds: dict[str, Fund], session):

        # Init result list
        result = []

        # loop through each fund ID
        for fundID in fundsWithoutPrice:

            try:
                downloadedQuot = AnalizyFund.downloadQuotation(
                    allFunds[fundID])
            except Exception as err:

                # Create method output details
                result.append(
                    {
                        "responseCode": 204,
                        "responseBody": {
                            "Status": "Failed to download quotation",
                            "Status Details": str(err),
                            "Fund ID": fundID
                        }
                    }
                )
                result[-1]["responseCode"] = 204
                result[-1]["responseBody"] = {}
                result[-1]["responseBody"]["Fund ID"] = fundID
                result[-1]["responseBody"]["Status"] = "Failed to download quotation"
                result[-1]["responseBody"]["Status Details"] = str(err)

                continue
            
            result.append({})
            # Insert quotation to DB
            result[-1]["responseCode"], result[-1]["responseBody"] = Price.insertQuotationRecords(
                downloadedQuot,
                session
            )

            # create success result entry
            result.append(
                {
                    "responseCode": 200,
                    "responseBody": {
                        "Status": "Quotation successfully added",
                        "Last Quotation Date": Dates.convertDateToString(
                            downloadedQuot["FundQuotation"][-1][AnalizyFund.RESPONSE_DATE_NAME]
                        ),
                        "Fund ID": fundID
                    }
                }
            )

        return result

    @staticmethod
    def insertQuotationRecords(dataToInsert: list[dict[str, str]], session, allQuotation=[]):

        # Loop through each quotation entry
        for entry in dataToInsert["FundQuotation"]:

            # Create local variables for quotation value and date
            currentDate = entry[AnalizyFund.RESPONSE_DATE_NAME]
            currentValue = entry[AnalizyFund.RESPONSE_PRICE_NAME]

            # Prepare dict to calculate refund in different periods
            result = {
                'daily': None,
                'weekly': None,
                'monthly': None,
                'yearly': None
            }

            # Get appropriate dates for particular result types
            # method calculates what date would be,
            # to have the result from day, week, month before current date
            dates = Dates.getDesiredDates(currentDate)

            # Loop through each calculated date
            for period in dates:

                # Get appropriate result to currently calculated refund period
                # if the result equals to None it means that there is no quotation for desired date
                if (prev_value := Dates.getEntryWithDesiredDate(
                    allQuotation + dataToInsert["FundQuotation"],
                    AnalizyFund.RESPONSE_DATE_NAME,
                    dates[period]
                )
                ) != None:

                    # Based on filtered data calculate result
                    result[period] = (
                        currentValue / prev_value[AnalizyFund.RESPONSE_PRICE_NAME]) - 1.0

            # Create DB entry
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

        responseCode = 200
        # try to commit all inserted data
        try:
            session.commit()
            result = {
                "Status": "Quotation successfully added",
                "Last Quotation Date": Dates.convertDateToString(
                    dataToInsert["FundQuotation"][-1][AnalizyFund.RESPONSE_DATE_NAME]
                )
            }

        except IndexError as indexErr:

            # Add success message as index error means that there were no new entries to insert
            result = {
                "Status": "No new quotation to add"
            }

        except Exception as err:

            # Rollback transaction to be able to successfully proceed with the next url
            session.rollback()

            # Add error message without further analysis
            result = {
                "Status": f"Failed to add quotation {type(err)}",
                "Status Details": str(err)
            }
            responseCode = 206

        return responseCode, result

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
