"""
.DESCRIPTION
    Main FLASK API file.
    

.NOTES

    Version:            1.2
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
    
"""

import os
from flask import Flask, jsonify, request, Response
from Processing.Price import Price
from Processing.InvestmentCalcResult import InvestmentCalcResult
from Processing.FundConfig import FundConfig
from Processing.InvestmentConfig import InvestmentConfig


app = Flask(__name__)

DEBUG_MODE = os.getenv('FLASK_DEBUG', True)


@app.route('/FundConfig', methods=['PUT', 'GET'])
def fund_handler():
    match request.method:

        case "PUT":
            jsonFunds = request.json
            responseCode, responseBody = FundConfig.insertFundConfig(jsonFunds)
            
            return responseBody, responseCode
        
        case "GET":
            responseCode, responseBody = FundConfig.getFundUrls()
            
            return responseBody, responseCode


@app.route('/FundQuotation', methods=['PUT'])
def quotation_handler():
    match request.method:
        
        case "PUT":
            responseCode, responseBody = Price.updateQuotation()

            return responseBody, responseCode


@app.route('/InvestmentConfig', methods=['PUT', 'GET'])
@app.route('/InvestmentConfig/<int:id>', methods=[ 'GET'])
def investment_handler(id: int = None):
    match request.method:
        
        case "PUT":
            jsonInvestments = request.json
            responseCode, responseBody = InvestmentConfig.insertInvestmentConfig(
                jsonInvestments["Investments"],
                jsonInvestments["Owner"]
            )

            return responseBody, responseCode
        
        case "GET":
            responseCode, responseBody = InvestmentConfig.getInvestmentFunds(id)
            
            return responseBody, responseCode


@app.route('/InvestmentRefund', methods=['PUT'])
@app.route('/InvestmentRefund/<int:id>', methods=['PUT'])
def refund_handler(id: int = None):
    match request.method:
        
        case "PUT":
            if id == None:
                responseCode, responseBody =  InvestmentCalcResult.calculateAllResults()
                
                return responseBody, responseCode
            else:
                responseCode, responseBody = InvestmentCalcResult.calculateResult(id)
                
                return responseBody, responseCode



if __name__ == '__main__':
    app.run(
        debug=DEBUG_MODE,
        host='0.0.0.0'
    )
