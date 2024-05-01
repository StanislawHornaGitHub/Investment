"""
.DESCRIPTION
    Main FLASK API file.
    

.NOTES

    Version:            1.3
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      30-Mar-2024
    ChangeLog:

    Date            Who                     What
    2024-04-03      Stanisław Horna         Response body and code implemented.
    
    2024-04-26      Stanisław Horna         Endpoint to get monitored fund urls with last quotation date implemented.
                                            Endpoint to refresh singular investment.
                                            Endpoint to get investment funds with last refund date implemented.
                                            Unified naming and structure.
    
    2024-04-30      Stanisław Horna         Add logging capabilities.
    
"""

import os
from Utility.Logger import logger
from Utility.SQL_connection_check import SQLhealthCheck
from flask import Flask, request
from Processing.Price import Price
from Processing.InvestmentCalcResult import InvestmentCalcResult
from Processing.FundConfig import FundConfig
from Processing.InvestmentConfig import InvestmentConfig


app = Flask(__name__)

FLASK_DEBUG_MODE = os.getenv('FLASK_DEBUG', True)


@app.route('/health', methods=['GET'])
def health_check():
    responseBody = {
        "Database is available": SQLhealthCheck.checkSQLConnection()
    }
    responseCode = 200
    if False in list(responseBody.values()):
        responseCode = 503

    return responseBody, responseCode


@app.route('/FundConfig', methods=['PUT', 'GET'])
@app.route('/FundConfig/<id>', methods=['GET'])
def fund_handler(id: str = None):

    logger.info("fund_handler(%s), method: %s", id, (request.method))

    match (request.method):

        case "PUT":
            logger.debug("Method: PUT")
            jsonFunds = request.json
            responseCode, responseBody = (
                FundConfig.insertFundConfig(jsonFunds)
            )

        case "GET":
            logger.debug("Method: GET")
            responseCode, responseBody = (
                FundConfig.getFund(id)
            )

    logger.debug(
        "fund_handler(%s). Returning body and code: %d",
        id,
        responseCode
    )
    return responseBody, responseCode


@app.route('/FundQuotation', methods=['PUT'])
@app.route('/FundQuotation/<id>', methods=['PUT'])
def quotation_handler(id: str = None):

    logger.info("quotation_handler(%s), method: %s", id, (request.method))

    match (request.method):

        case "PUT":
            logger.debug("Method: PUT")
            responseCode, responseBody = (
                Price.updateQuotation(id)
            )

    logger.debug(
        "quotation_handler(%s). Returning body and code: %d",
        id,
        responseCode
    )
    return responseBody, responseCode


@app.route('/InvestmentConfig', methods=['PUT', 'GET'])
@app.route('/InvestmentConfig/<int:id>', methods=['GET'])
def investment_handler(id: int = None):

    logger.info("investment_handler(%s), method: %s", id, (request.method))

    match (request.method):

        case "PUT":
            logger.debug("Method: PUT")

            jsonInvestments = request.json
            responseCode, responseBody = (
                InvestmentConfig.insertInvestmentConfig(
                    jsonInvestments["Investments"],
                    jsonInvestments["Owner"]
                )
            )

        case "GET":
            logger.debug("Method: GET")
            responseCode, responseBody = (
                InvestmentConfig.getInvestmentFunds(id)
            )

    logger.debug(
        "investment_handler(%s). Returning body and code: %d",
        id,
        responseCode
    )
    return responseBody, responseCode


@app.route('/InvestmentRefund', methods=['PUT'])
@app.route('/InvestmentRefund/<int:id>', methods=['PUT'])
def refund_handler(id: int = None):

    logger.info("refund_handler(%s), method: %s", id, (request.method))

    match (request.method):

        case "PUT":
            if id is None:
                logger.debug("Method: PUT, ID is none")
                responseCode, responseBody = (
                    InvestmentCalcResult.calculateAllResults()
                )
            else:
                logger.debug("Method: PUT, ID is NOT none")
                responseCode, responseBody = (
                    InvestmentCalcResult.calculateResult(id)
                )

    logger.debug(
        "investment_handler(%s). Returning body and code: %d",
        id,
        responseCode
    )
    return responseBody, responseCode


if __name__ == '__main__':
    app.run(
        debug=FLASK_DEBUG_MODE,
        host='0.0.0.0'
    )
