"""
.DESCRIPTION
    Class definition to interact with Analizy.PL API.
    

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      28-Apr-2024
    ChangeLog:

    Date            Who                     What
    2024-04-29      Stanisław Horna         Add logging capabilities.

"""

import requests
import datetime
from dateutil.parser import parse
from dataclasses import dataclass, field
from Utility.Exceptions import AnalizyAPIexception
from Utility.Logger import logger


@dataclass
class AnalizyAPI:

    __API_URL = "https://www.analizy.pl/api/quotation"

    __RESPONSE_DETAILS = "series"
    __RESPONSE_LIST = "price"
    __RESPONSE_DATE_NAME = "date"

    @staticmethod
    def getLastQuotationDate(fund_id: str, fund_category: str) -> datetime.date:

        logger.debug("getLastQuotationDate(%s, %s)", fund_id, fund_category)

        # Create custom URL to access API to download JSON with all quotation
        url = f"{AnalizyAPI.__API_URL}/{fund_category}/{fund_id}"

        try:
            # Invoke web request and convert JSON response to dict
            logger.debug("Calling %s", url)
            apiResponse = requests.get(url)
            logger.debug("Response status code: %d", apiResponse.status_code)
            fundQuotation = apiResponse.json()
        except Exception as err:
            logger.exception("Exception occurred", exc_info=True)
            raise AnalizyAPIexception(str(err))

        logger.debug("Parsing %s", AnalizyAPI.__RESPONSE_DATE_NAME)
        quotation = fundQuotation[AnalizyAPI.__RESPONSE_DETAILS][0][AnalizyAPI.__RESPONSE_LIST]

        lastDate = parse(
            quotation[-1][AnalizyAPI.__RESPONSE_DATE_NAME]
        ).date()

        logger.debug("Returning date for fund: %s", fund_id)
        return lastDate
