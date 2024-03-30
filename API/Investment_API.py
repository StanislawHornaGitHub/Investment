from flask import Flask, jsonify, request 
import SQL
from Processing.Price import Price
from Processing.InvestmentCalcResult import InvestmentCalcResult
from Processing.FundConfig import FundConfig

app = Flask(__name__) 

@app.route('/FundQuotation', methods=['PUT']) 
def refreshFundQuotation(): 
	if(request.method == 'PUT'): 
		Price.updateQuotation()
		data = {"status": "Refreshed"} 
		return jsonify(data) 

@app.route('/InvestmentRefund', methods=['PUT']) 
def refreshInvestmentRefund(): 
	if(request.method == 'PUT'): 
		InvestmentCalcResult.calculateAllResults()
		data = {"status": "Refreshed"} 
		return jsonify(data) 

@app.route('/FundConfig', methods=['PUT']) 
def insertFundURL(): 
	if(request.method == 'PUT'): 
		jsonFunds = request.json
		FundConfig.insertFundConfig(jsonFunds)
		return jsonFunds

if __name__ == '__main__': 
	app.run(debug=True, host='0.0.0.0') 
