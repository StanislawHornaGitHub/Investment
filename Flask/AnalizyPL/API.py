"""
.DESCRIPTION
    Class definition for static methods related to communication with Analizy.PL API,
    to download fund quotation.
    

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      24-Mar-2024
    ChangeLog:

    Date            Who                     What
    2024-04-30      Stanisław Horna         Add logging capabilities.

"""
import logging
from dataclasses import dataclass, field
from SQL.Fund import Fund
from SQL.Quotation import Quotation
import json
import requests
from dateutil.parser import parse


@dataclass
class AnalizyFundAPI:

    __API_URL = "https://www.analizy.pl/api/quotation"

    RESPONSE_ID = "id"
    RESPONSE_CURRENCY = "currency"
    RESPONSE_DETAILS = "series"
    RESPONSE_LIST = "price"
    RESPONSE_DATE_NAME = "date"
    RESPONSE_PRICE_NAME = "value"

    @staticmethod
    def downloadQuotation(fund: Fund) -> list[Quotation]:

        logging.debug("downloadQuotation(%s)", fund.getFundID())

        # Create custom URL to access API to download JSON with all quotation
        URL = f"{AnalizyFundAPI.__API_URL}/{fund.getFundCategoryShort()}/{fund.getFundID()}"

        # Invoke web request and convert JSON response to dict
        try:
            fundQuotationResponse = json.loads(requests.get(URL).content)
        except:
            logging.exception(exc_info=True)
            return None

        fundID = fundQuotationResponse[AnalizyFundAPI.RESPONSE_ID]

        result = {
            "Fund_ID": fundID,
            "Fund_Currency": None,
            "FundQuotation": (
                fundQuotationResponse[AnalizyFundAPI.RESPONSE_DETAILS][0][AnalizyFundAPI.RESPONSE_LIST]
            )
        }

        logging.debug(
            "Converting str types to proper ones (%s, %s)",
            AnalizyFundAPI.RESPONSE_DATE_NAME,
            AnalizyFundAPI.RESPONSE_PRICE_NAME
        )
        for i in range(len(result["FundQuotation"])):
            result["FundQuotation"][i][AnalizyFundAPI.RESPONSE_DATE_NAME] = parse(
                result["FundQuotation"][i][AnalizyFundAPI.RESPONSE_DATE_NAME]
            )
            result["FundQuotation"][i][AnalizyFundAPI.RESPONSE_PRICE_NAME] = float(
                result["FundQuotation"][i][AnalizyFundAPI.RESPONSE_PRICE_NAME]
            )

        logging.debug("Returning quotation")
        return result
