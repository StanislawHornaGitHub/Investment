"""
.DESCRIPTION
    Class definition for static methods related downloading fund quotation from the Internet.

.NOTES

    Version:            1.2
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      24-Mar-2024
    ChangeLog:

    Date            Who                     What
    2024-04-02      Stanisław Horna         Response body and code implemented.
    
    2024-04-30      Stanisław Horna         Add logging capabilities.

"""
import SQL
import logging
from SQL.Quotation import Quotation
from SQL.Fund import Fund
from AnalizyPL.API import AnalizyFundAPI
from Utility.ConvertToDict import ConvertToDict
from sqlalchemy import func

from Utility.Dates import Dates


class Price:

    @staticmethod
    def updateQuotation(ID: str = None):

        logging.debug("updateQuotation(%s)", ID)

        # Create session and init processing variables
        session = SQL.base.Session()
        responseCode = 200
        result = []

        if ID is None:

            logging.debug("ID is none")

            # Get monitored Fund IDs
            fund = ConvertToDict.fundList(session.query(Fund).all())

            # Get last quotation date for each fund
            lastRefreshDates = (
                session
                .query(func.max(Quotation.date), Quotation.fund_id)
                .group_by(Quotation.fund_id)
                .all()
            )
        else:

            logging.debug("ID is not none")

            # Check if provided ID exists in DB
            if (Fund.IDisValid(ID, session) != True):
                logging.error("Fund with ID: %s does not exist", ID)
                resultBody = {
                    "fund_id": ID,
                    "Status": f"Fund with ID: {ID} does not exist"
                }
                responseCode = 404

                logging.debug(
                    "updateQuotation(%s), returning result body and code: %d",
                    ID,
                    responseCode
                )
                return responseCode, resultBody

            # Get monitored Fund IDs
            try:
                fund = ConvertToDict.fundList(
                    (
                        session
                        .query(Fund)
                        .filter(Fund.fund_id == ID)
                        .all()
                    )
                )
            except:
                logging.exception(
                    "Failed to get list of monitored funds",
                    exc_info=True
                )
                return None, None

            # Get last quotation date for each fund
            try:
                lastRefreshDates = (
                    session
                    .query(func.max(Quotation.date), Quotation.fund_id)
                    .filter(Quotation.fund_id == ID)
                    .group_by(Quotation.fund_id)
                    .all()
                )
            except:
                logging.exception(
                    "Failed to get funds' last refresh dates",
                    exc_info=True
                )

        # Loop through each fund which already has some quotation in DB
        for date, fundID in lastRefreshDates:

            logging.debug("Processing (date | fund ID) %s | %s", date, fundID)
            # Download newest quotation from Analizy.pl
            downloadedQuot = AnalizyFundAPI.downloadQuotation(fund[fundID])

            if downloadedQuot is None:
                responseCode = 204
                logging.error(
                    "Failed to download quotation for fund: %s",
                    fundID
                )
                result.append(
                    {
                        "fund_id": fundID,
                        "Status": "Failed to download quotation"
                    }
                )
                continue

            # Create temp variable to store all downloaded quotation
            allQuotations = downloadedQuot["FundQuotation"]

            logging.debug("Filtering quotation to get newer then %s", date)
            # Filter out the quotation to only those entries which will be inserted to DB
            downloadedQuot["FundQuotation"] = [
                q for q in downloadedQuot["FundQuotation"]
                if q[AnalizyFundAPI.RESPONSE_DATE_NAME] > date
            ]

            # Insert quotation to DB
            code, responseBody = Price.insertQuotationRecords(
                downloadedQuot,
                session,
                allQuotations
            )

            responseBody["fund_id"] = fundID

            result.append(responseBody)

            if code != 204:
                responseCode = code
        logging.debug("Filtering out funds without quotations saved in DB")
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

        logging.debug("insertQuotation(%s)", str(fundsWithoutPrice))

        # Init result list
        result = []

        # loop through each fund ID
        for fundID in fundsWithoutPrice:

            logging.debug("Processing: %s", fundID)

            downloadedQuot = AnalizyFundAPI.downloadQuotation(
                allFunds[fundID]
            )

            if downloadedQuot is None:
                logging.error(
                    "Failed to download quotation for fund: %s",
                    fundID
                )
                # Create method output details
                result.append(
                    {
                        "responseCode": 204,
                        "responseBody": {
                            "Status": "Failed to download quotation",
                            "fund_id": fundID
                        }
                    }
                )
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
                            downloadedQuot["FundQuotation"][-1][AnalizyFundAPI.RESPONSE_DATE_NAME]
                        ),
                        "fund_id": fundID
                    }
                }
            )
        logging.debug("insertQuotation(%s). Returning", str(fundsWithoutPrice))
        return result

    @staticmethod
    def insertQuotationRecords(dataToInsert: list[dict[str, str]], session, allQuotation=[]):

        logging.debug("insertQuotationRecords()")
        # Loop through each quotation entry
        for entry in dataToInsert["FundQuotation"]:

            # Create local variables for quotation value and date
            currentDate = entry[AnalizyFundAPI.RESPONSE_DATE_NAME]
            currentValue = entry[AnalizyFundAPI.RESPONSE_PRICE_NAME]

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
                    AnalizyFundAPI.RESPONSE_DATE_NAME,
                    dates[period]
                )
                ) != None:

                    # Based on filtered data calculate result
                    result[period] = (
                        currentValue / prev_value[AnalizyFundAPI.RESPONSE_PRICE_NAME]) - 1.0

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
                    dataToInsert["FundQuotation"][-1][AnalizyFundAPI.RESPONSE_DATE_NAME]
                )
            }

        except IndexError as indexErr:
            logging.warning("No new quotation to add", exc_info=True)
            # Add success message as index error means that there were no new entries to insert
            result = {
                "Status": "No new quotation to add"
            }

        except Exception as err:
            logging.exception("Failed to add quotation", exc_info=True)
            # Rollback transaction to be able to successfully proceed with the next url
            session.rollback()

            # Add error message without further analysis
            result = {
                "Status": f"Failed to add quotation {type(err)}",
                "status_details": str(err)
            }
            responseCode = 206

        logging.debug(
            "insertQuotationRecords(). Returning body and code: %d",
            responseCode
        )
        return responseCode, result
