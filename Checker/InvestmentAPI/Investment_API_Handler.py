"""
.DESCRIPTION
    Class definition with static definition to interact with Investment API.


.NOTES

    Version:            1.2
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      27-Apr-2024
    ChangeLog:

    Date            Who                     What
    2024-04-29      Stanisław Horna         Add logging capabilities.
    
    2024-05-14      Stanisław Horna         Add new methods to put funds and investments to system.

"""
import os
import requests
import time
import json
from Log.Logger import logger
from datetime import date
from dateutil.parser import parse
from Utility.Exceptions import InvestmentAPIexception


class InvestmentAPI:

    __API_IP = os.getenv('FLASK_IP_Address', 'localhost')
    __API_PORT = os.getenv('FLASK_Port', '5000')

    __FUND_ENDPOINT = "FundConfig"
    __FUND_RESP_DATE = "quotation_date"

    __INVESTMENT_ENDPOINT = "InvestmentConfig"
    __INVESTMENT_RESP_DATE = "refund_date"

    __QUOTATION_ENDPOINT = "FundQuotation"

    __REFUND_ENDPOINT = "InvestmentRefund"

    @staticmethod
    def waitForFullSystemInitialization():

        logger.info("Waiting for system initialization.")

        # loop until request to get funds will be successful
        while True:
            try:
                logger.info("Number of funds: %c", str(
                    len(InvestmentAPI.getFunds())))
                logger.info("System is up and running.")
                return
            except InvestmentAPIexception:
                logger.exception(
                    "InvestmentAPI exception occurred", exc_info=True)
                time.sleep(5)
                continue

    @staticmethod
    def getFunds(ID: str = None) -> list[dict[str, str | date]]:

        logger.debug("getFunds(%s)", ID)

        # create appropriate url whether ID was provided or not
        if ID is None:
            logger.debug("URL for fund is none created")
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__FUND_ENDPOINT}"
        else:
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__FUND_ENDPOINT}/{ID}"
            logger.debug("URL for fund is NOT none created")

        # call API
        logger.debug("Calling %s", url)
        apiResponse = requests.get(url)
        logger.debug("Response status code: %d", apiResponse.status_code)
        result = apiResponse.json()

        # check response code
        if apiResponse.status_code == 200:

            logger.debug(
                "Parsing %s to datetime type",
                InvestmentAPI.__FUND_RESP_DATE
            )
            # loop through returned list and convert date from sting to datetime
            for i in range(0, len(result)):
                result[i][InvestmentAPI.__FUND_RESP_DATE] = parse(
                    result[i][InvestmentAPI.__FUND_RESP_DATE]
                ).date()

        else:
            # raise an exception if status code was different than 200
            raise InvestmentAPIexception(str(result))

        logger.debug("Returning fund list")
        return result

    @staticmethod
    def updateFunds(ID: str = None) -> list[dict[str, str | date]]:

        logger.debug("updateFunds(%s)", ID)

        # create appropriate url whether ID was provided or not
        if ID is None:
            logger.debug("URL for fund is none created")
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__QUOTATION_ENDPOINT}"
        else:
            logger.debug("URL for fund is NOT none created")
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__QUOTATION_ENDPOINT}/{ID}"

        # call API
        logger.debug("Calling %s", url)
        apiResponse = requests.put(url)
        logger.debug("Response status code: %d", apiResponse.status_code)
        result = apiResponse.json()

        if apiResponse.status_code != 200:

            raise InvestmentAPIexception(result)

        logger.debug("Returning update status")
        return result

    @staticmethod
    def getInvestment(ID: int = None) -> list[dict[str, str | date]]:

        logger.debug("getInvestment(%s)", ID)

        # create appropriate url whether ID was provided or not
        if ID is None:
            logger.debug("URL for investment is none created")
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__INVESTMENT_ENDPOINT}"
        else:
            logger.debug("URL for investment is NOT none created")
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__INVESTMENT_ENDPOINT}/{ID}"

        # call API
        logger.debug("Calling %s", url)
        apiResponse = requests.get(url)
        logger.debug("Response status code: %d", apiResponse.status_code)
        result = apiResponse.json()

        # check response code
        if apiResponse.status_code == 200:

            logger.debug("Parsing %s to datetime type",
                         InvestmentAPI.__INVESTMENT_RESP_DATE)
            # loop through returned list and convert date from sting to datetime
            for i in range(0, len(result)):
                result[i][InvestmentAPI.__INVESTMENT_RESP_DATE] = parse(
                    result[i][InvestmentAPI.__INVESTMENT_RESP_DATE]
                ).date()

        else:
            raise InvestmentAPIexception(str(result))

        logger.debug("Returning investment list")
        return result

    @staticmethod
    def updateInvestment(ID: int = None) -> list[dict[str, str | date]]:

        logger.debug("updateInvestment(%s)", ID)

        # create appropriate url whether ID was provided or not
        if ID is None:
            logger.debug("URL for investment is none created")
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__REFUND_ENDPOINT}"
        else:
            logger.debug("URL for investment is NOT none created")
            url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__REFUND_ENDPOINT}/{ID}"

        # call API
        logger.debug("Calling %s", url)
        apiResponse = requests.put(url)
        logger.debug("Response status code: %d", apiResponse.status_code)
        result = apiResponse.json()

        if apiResponse.status_code != 200:

            raise InvestmentAPIexception(result)

        logger.debug("Returning update status")
        return result

    @staticmethod
    def putFunds(data: list[str]):
        logger.debug("importFunds(%s)", data)

        # create appropriate url
        url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__FUND_ENDPOINT}"

        # dump provided data into json structure
        try:
            json_data = json.dumps(data)
        except Exception as e:
            logger.exception(
                "Failed to dump provided data to json",
                exc_info=True
            )
            raise InvestmentAPIexception(e)

        # call api
        logger.debug("Calling %s", url)
        apiResponse = requests.put(
            url,
            data=json_data,
            headers={'Content-Type': 'application/json'}
        )
        logger.debug("Response status code: %d", apiResponse.status_code)

        result = apiResponse.json()
        if apiResponse.status_code not in (200, 206):

            raise InvestmentAPIexception(result)

        logger.debug("Returning PUT response")
        return result

    @staticmethod
    def putInvestments(data: list[dict[str, dict[str, list[str]]]]):

        logger.debug("importInvestments(%s)", data)

        # create appropriate url
        url = f"http://{InvestmentAPI.__API_IP}:{InvestmentAPI.__API_PORT}/{InvestmentAPI.__INVESTMENT_ENDPOINT}"
        try:
            json_data = json.dumps(data)
        except Exception as e:
            logger.exception(
                "Failed to dump provided data to json",
                exc_info=True
            )
            raise InvestmentAPIexception(e)

        # call API
        logger.debug("Calling %s", url)
        apiResponse = requests.put(
            url,
            data=json_data,
            headers={'Content-Type': 'application/json'}
        )
        logger.debug("Response status code: %d", apiResponse.status_code)

        result = apiResponse.json()
        if apiResponse.status_code not in (200, 206):

            raise InvestmentAPIexception(result)

        logger.debug("Returning PUT response")
        return result
