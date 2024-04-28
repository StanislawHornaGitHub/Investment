"""
.DESCRIPTION
    Class definition with static definition to interact with Analizy.PL website.
    

.NOTES

    Version:            1.0
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


class AnalizyFundFront:

    __X_FILTER_UPDATE_DATE = '//p[@class="lightProductText"]/text()'

    @staticmethod
    def getLastQuotationDate(url: str) -> datetime.date:
        
        # Invoke web request to provided URL
        try:
            response = requests.get(url)
        except:
            return None
        
        # Convert response to HTML tree
        treeHTML = fromstring(response.content)

        # Read out date from HTML and convert it to proper type
        date = parse(
            str(
                treeHTML.xpath(AnalizyFundFront.__X_FILTER_UPDATE_DATE)[0]
            )
            .strip()
        ).date()
        
        return date
