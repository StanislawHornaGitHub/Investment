"""
.DESCRIPTION
    Class definition with static definition to interact with Investment API.
    

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      27-Apr-2024
    ChangeLog:

    Date            Who                     What
    2024-04-29      Stanisław Horna         Add logging capabilities.

"""
import os
import requests
import time
import logging
from datetime import date
from dateutil.parser import parse
from Utility.Exceptions import InvestmentAPIexception

class InvestmentAPI:
    
    __API_IP = os.getenv('FLASK_IP_Address', '192.168.0.212')
    __API_PORT = os.getenv('FLASK_Port', '5000')

    __FUND_ENDPOINT = "FundConfig"
    __FUND_RESP_DATE = "quotation_date"

    __INVESTMENT_ENDPOINT = "InvestmentConfig"
    __INVESTMENT_RESP_DATE = "refund_date"
    
    __QUOTATION_ENDPOINT = "FundQuotation"
    
    __REFUND_ENDPOINT = "InvestmentRefund"

    @staticmethod
    def waitForFullSystemInitialization():
        
        logging.info("Waiting for system initialization.")
        
        # loop until request to get funds will be successful
        while True:
            try:
                logging.info("API response: %s",str(InvestmentAPI.getFunds()))
                logging.info("System is up and running.")
                return
            except InvestmentAPIexception as invErr:
                logging.warning("InvestmentAPI exception occurred", exc_info=True)
                time.sleep(5)
                continue

    @staticmethod
    def getFunds(ID: str = None) -> list[dict[str, str | date]]:
        
        logging.info("getFunds(%s)", ID)

        # Create appropriate url whether ID was provided or not
        if ID is None:
            logging.info("URL for fund is none created")
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__FUND_ENDPOINT}"
        else:
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__FUND_ENDPOINT}/{ID}"
            logging.info("URL for fund is NOT none created")

        # Call API
        logging.info("Calling %s", url)
        apiResponse = requests.get(url)
        logging.info("Response status code: %d", apiResponse.status_code)
        result = apiResponse.json()

        # Check response code
        if apiResponse.status_code == 200:
            
            logging.info("Parsing %s to datetime type", InvestmentAPI.__FUND_RESP_DATE)
            # Loop through returned list and convert date from sting to datetime
            for i in range(0, len(result)):
                result[i][InvestmentAPI.__FUND_RESP_DATE] = parse(
                    result[i][InvestmentAPI.__FUND_RESP_DATE]
                ).date()

        else:
            # Raise an exception if status code was different than 200
            logging.error("Request was NOT successful: %s", str(result))
            raise InvestmentAPIexception(str(result))
        
        logging.info("Returning fund list")
        return result
    
    @staticmethod
    def updateFunds(ID: str = None):
        
        logging.info("updateFunds(%s)", ID)
        
        # Create appropriate url whether ID was provided or not
        if ID is None:
            logging.info("URL for fund is none created")
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__QUOTATION_ENDPOINT}"
        else:
            logging.info("URL for fund is NOT none created")
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__QUOTATION_ENDPOINT}/{ID}"
        
        # Call API
        logging.info("Calling %s", url)
        apiResponse = requests.put(url)
        logging.info("Response status code: %d", apiResponse.status_code)
        result = apiResponse.json()
        
        if apiResponse.status_code != 200:
            
            logging.error("Update was NOT successful: %s", str(result))
            raise InvestmentAPIexception(result)
        
        logging.info("Returning update status")
        return result

    @staticmethod
    def getInvestment(ID: int = None) -> list[dict[str, str | date]]:
        
        logging.info("getInvestment(%s)", ID)
        
        # Create appropriate url whether ID was provided or not
        if ID is None:
            logging.info("URL for investment is none created")
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__INVESTMENT_ENDPOINT}"
        else:
            logging.info("URL for investment is NOT none created")
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__INVESTMENT_ENDPOINT}/{ID}"

        # Call API
        logging.info("Calling %s", url)
        apiResponse = requests.get(url)
        logging.info("Response status code: %d", apiResponse.status_code)
        result = apiResponse.json()

        # Check response code
        if apiResponse.status_code == 200:
            
            logging.info("Parsing %s to datetime type", InvestmentAPI.__INVESTMENT_RESP_DATE)
            # Loop through returned list and convert date from sting to datetime
            for i in range(0, len(result)):
                result[i][InvestmentAPI.__INVESTMENT_RESP_DATE] = parse(
                    result[i][InvestmentAPI.__INVESTMENT_RESP_DATE]
                ).date()

        else:
            logging.error("Request was NOT successful: %s", str(result))
            raise InvestmentAPIexception(str(result))
        
        logging.info("Returning investment list")
        return result
    
    @staticmethod
    def updateInvestment(ID: int = None):
        
        logging.info("updateInvestment(%s)", ID)
        
        # Create appropriate url whether ID was provided or not
        if ID is None:
            logging.info("URL for investment is none created")
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__REFUND_ENDPOINT}"
        else:
            logging.info("URL for investment is NOT none created")
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__REFUND_ENDPOINT}/{ID}"

        # Call API
        logging.info("Calling %s", url)
        apiResponse = requests.put(url)
        logging.info("Response status code: %d", apiResponse.status_code)
        result = apiResponse.json()
        
        if apiResponse.status_code != 200:
            
            logging.error("Update was NOT successful: %s", str(result))
            raise InvestmentAPIexception(result)
        
        logging.info("Returning update status")
        return result