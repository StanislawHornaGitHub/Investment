"""
.DESCRIPTION
    Main FLASK API file.
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      30-Mar-2024
    ChangeLog:

    Date            Who                     What

"""

import os
from flask import Flask, jsonify, request, Response
from Processing.Price import Price
from Processing.InvestmentCalcResult import InvestmentCalcResult
from Processing.FundConfig import FundConfig
from Processing.InvestmentConfig import InvestmentConfig

app = Flask(__name__)

DEBUG_MODE = os.getenv('FLASK_DEBUG', True)


@app.route('/FundQuotation', methods=['PUT'])
def refreshFundQuotation():
    if (request.method == 'PUT'):
        responseCode, responseBody = Price.updateQuotation()
        
        return responseBody, responseCode


@app.route('/InvestmentRefund', methods=['PUT'])
def refreshInvestmentRefund():
    if (request.method == 'PUT'):
        InvestmentCalcResult.calculateAllResults()
        data = {"status": "Refreshed"}
        return jsonify(data)


@app.route('/FundConfig', methods=['PUT'])
def insertFundURL():
    if (request.method == 'PUT'):
        jsonFunds = request.json
        responseCode, responseBody = FundConfig.insertFundConfig(jsonFunds)

        return responseBody, responseCode


@app.route('/InvestmentConfig', methods=['PUT'])
def insertInvestmentConfig():
    if (request.method == 'PUT'):
        jsonInvestments = request.json
        InvestmentConfig.insertInvestmentConfig(
            jsonInvestments["Investments"],
            jsonInvestments["Owner"]
        )

        return jsonInvestments


if __name__ == '__main__':
    app.run(
        debug=DEBUG_MODE,
        host='0.0.0.0'
    )
