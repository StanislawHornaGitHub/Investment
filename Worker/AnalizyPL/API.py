from dataclasses import dataclass, field
from SQL.Fund import Fund
from SQL.Quotation import Quotation
import json
import requests
from dateutil.parser import parse


@dataclass
class AnalizyFund:
    
    API_URL = "https://www.analizy.pl/api/quotation"
    
    RESPONSE_ID = "id"
    RESPONSE_CURRENCY = "currency"
    RESPONSE_DETAILS = "series"
    RESPONSE_LIST = "price"
    RESPONSE_DATE_NAME = "date"
    RESPONSE_PRICE_NAME = "value"
    
    @staticmethod
    def downloadQuotation(fund: Fund) -> list[Quotation]:

        # Create custom URL to access API to download JSON with all quotation
        URL = f"{AnalizyFund.API_URL}/{fund.getFundCategoryShort()}/{fund.getFundID()}"

        # Invoke web request and convert JSON response to dict
        fundQuotationResponse = json.loads(requests.get(URL).content)
        fundID = fundQuotationResponse[AnalizyFund.RESPONSE_ID]
        
        result = {
            "Fund_ID": fundID,
            "Fund_Currency": None,
            "FundQuotation": fundQuotationResponse[AnalizyFund.RESPONSE_DETAILS][0][AnalizyFund.RESPONSE_LIST]
        }

        return result