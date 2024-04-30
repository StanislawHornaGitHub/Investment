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
import logging
from flask import Flask, jsonify, request, Response
from Processing.Price import Price
from Processing.InvestmentCalcResult import InvestmentCalcResult
from Processing.FundConfig import FundConfig
from Processing.InvestmentConfig import InvestmentConfig


app = Flask(__name__)

FLASK_DEBUG_MODE = os.getenv('FLASK_DEBUG', True)
LOG_LEVEL = os.getenv('LOG_LEVEL', "DEBUG")

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d - %(levelname)s - PID: %(process)d - %(module)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=LOG_LEVEL
)


@app.route('/FundConfig', methods=['PUT', 'GET'])
@app.route('/FundConfig/<id>', methods=['GET'])
def fund_handler(id: str = None):

    logging.info("fund_handler(%s), method: %s", id, (request.method))

    match (request.method):

        case "PUT":
            logging.debug("Method: PUT")
            jsonFunds = request.json
            responseCode, responseBody = (
                FundConfig.insertFundConfig(jsonFunds)
            )

        case "GET":
            logging.debug("Method: GET")
            responseCode, responseBody = (
                FundConfig.getFund(id)
            )

    logging.debug(
        "fund_handler(%s). Returning body and code: %d",
        id,
        responseCode
    )
    return responseBody, responseCode


@app.route('/FundQuotation', methods=['PUT'])
@app.route('/FundQuotation/<id>', methods=['PUT'])
def quotation_handler(id: str = None):

    logging.info("quotation_handler(%s), method: %s", id, (request.method))

    match (request.method):

        case "PUT":
            logging.debug("Method: PUT")
            responseCode, responseBody = (
                Price.updateQuotation(id)
            )

    logging.debug(
        "quotation_handler(%s). Returning body and code: %d",
        id,
        responseCode
    )
    return responseBody, responseCode


@app.route('/InvestmentConfig', methods=['PUT', 'GET'])
@app.route('/InvestmentConfig/<int:id>', methods=['GET'])
def investment_handler(id: int = None):

    logging.info("investment_handler(%s), method: %s", id, (request.method))

    match (request.method):

        case "PUT":
            logging.debug("Method: PUT")

            jsonInvestments = request.json
            responseCode, responseBody = (
                InvestmentConfig.insertInvestmentConfig(
                    jsonInvestments["Investments"],
                    jsonInvestments["Owner"]
                )
            )

        case "GET":
            logging.debug("Method: GET")
            responseCode, responseBody = (
                InvestmentConfig.getInvestmentFunds(id)
            )

    logging.debug(
        "investment_handler(%s). Returning body and code: %d",
        id,
        responseCode
    )
    return responseBody, responseCode


@app.route('/InvestmentRefund', methods=['PUT'])
@app.route('/InvestmentRefund/<int:id>', methods=['PUT'])
def refund_handler(id: int = None):

    logging.info("refund_handler(%s), method: %s", id, (request.method))

    match (request.method):

        case "PUT":
            logging.debug("Method: PUT")
            if id is None:
                logging.debug("ID is none")
                responseCode, responseBody = (
                    InvestmentCalcResult.calculateAllResults()
                )
            else:
                logging.debug("ID is NOT none")
                responseCode, responseBody = (
                    InvestmentCalcResult.calculateResult(id)
                )

    logging.debug(
        "investment_handler(%s). Returning body and code: %d",
        id,
        responseCode
    )
    return responseBody, responseCode


if __name__ == '__main__':
    logging.info("Flask startup")
    app.run(
        debug=FLASK_DEBUG_MODE,
        host='0.0.0.0'
    )
