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

"""
import requests
from lxml.html import fromstring
import datetime
from dateutil.parser import parse


from dataclasses import dataclass, field



@dataclass
class AnalizyAPI:
    
    __API_URL = "https://www.analizy.pl/api/quotation"
    

    __RESPONSE_DETAILS = "series"
    __RESPONSE_LIST = "price"
    __RESPONSE_DATE_NAME = "date"
    
    @staticmethod
    def getLastQuotationDate(fund_id: str, fund_category: str) -> datetime.date:

        # Create custom URL to access API to download JSON with all quotation
        url = f"{AnalizyAPI.__API_URL}/{fund_category}/{fund_id}"

        # Invoke web request and convert JSON response to dict
        apiResponse = requests.get(url)
        
        fundQuotation = apiResponse.json()
        
        quotation = fundQuotation[AnalizyAPI.__RESPONSE_DETAILS][0][AnalizyAPI.__RESPONSE_LIST]
        
        lastDate = parse(
            quotation[-1][AnalizyAPI.__RESPONSE_DATE_NAME]
        ).date()
        
        return lastDate