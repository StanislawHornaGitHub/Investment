"""
.DESCRIPTION
    Class definition with static definition to interact with Investment API.
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      27-Apr-2024
    ChangeLog:

    Date            Who                     What

"""

import requests
from datetime import date
from dateutil.parser import parse


class InvestmentAPI:
    
    __API_PORT = 5000
    __API_IP = "192.168.0.212"

    __FUND_ENDPOINT = "FundConfig"
    __FUND_RESP_DATE = "quotation_date"

    __INVESTMENT_ENDPOINT = "InvestmentConfig"
    __INVESTMENT_RESP_DATE = "refund_date"
    
    __QUOTATION_ENDPOINT = "FundQuotation"
    
    __REFUND_ENDPOINT = "InvestmentRefund"

    @staticmethod
    def getFunds() -> list[dict[str, str | date]]:

        # Create appropriate url to call
        url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__FUND_ENDPOINT}"

        # Call API
        apiResponse = requests.get(url)
        result = apiResponse.json()

        # Check response code
        if apiResponse.status_code == 200:

            # Loop through returned list and convert date from sting to datetime
            for i in range(0, len(result)):
                result[i][InvestmentAPI.__FUND_RESP_DATE] = parse(
                    result[i][InvestmentAPI.__FUND_RESP_DATE]
                ).date()

        else:
            # Raise an exception if status code was different than 200
            raise Exception(str(result))
        
        return result
    
    @staticmethod
    def updateFunds(ID: str = None):
        
        # Create appropriate url whether ID was provided or not
        if ID is None:
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__QUOTATION_ENDPOINT}"
        else:
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__QUOTATION_ENDPOINT}/{ID}"
        
        # Call API
        apiResponse = requests.put(url)
        result = apiResponse.json()
        
        if apiResponse.status_code != 200:
            
            raise Exception(result)
        
        return result

    @staticmethod
    def getInvestment(ID: int = None) -> list[dict[str, str | date]]:
        
        # Create appropriate url whether ID was provided or not
        if ID is None:
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__INVESTMENT_ENDPOINT}"
        else:
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__INVESTMENT_ENDPOINT}/{ID}"

        # Call API
        apiResponse = requests.get(url)
        result = apiResponse.json()

        # Check response code
        if apiResponse.status_code == 200:

            # Loop through returned list and convert date from sting to datetime
            for i in range(0, len(result)):
                result[i][InvestmentAPI.__INVESTMENT_RESP_DATE] = parse(
                    result[i][InvestmentAPI.__INVESTMENT_RESP_DATE]
                ).date()

        else:
            raise Exception(str(result))
        
        return result
    
    @staticmethod
    def updateInvestment(ID: int = None):
        
        # Create appropriate url whether ID was provided or not
        if ID is None:
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__REFUND_ENDPOINT}"
        else:
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__REFUND_ENDPOINT}/{ID}"

        # Call API
        apiResponse = requests.put(url)
        result = apiResponse.json()
        
        if apiResponse.status_code != 200:
            
            raise Exception(result)
        
        return result