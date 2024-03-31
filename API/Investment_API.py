
import os
from flask import Flask, jsonify, request
from Processing.Price import Price
from Processing.InvestmentCalcResult import InvestmentCalcResult
from Processing.FundConfig import FundConfig
from Processing.InvestmentConfig import InvestmentConfig

app = Flask(__name__)

DEBUG_MODE = os.getenv('FLASK_DEBUG', True)

@app.route('/FundQuotation', methods=['PUT'])
def refreshFundQuotation():
    if (request.method == 'PUT'):
        Price.updateQuotation()
        data = {"status": "Refreshed"}
        return jsonify(data)


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
        FundConfig.insertFundConfig(jsonFunds)
        return jsonFunds


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
