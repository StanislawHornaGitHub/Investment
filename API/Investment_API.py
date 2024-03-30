from flask import Flask, jsonify, request 
import SQL
from Processing.InvestmentConfig import InvestmentConfig

app = Flask(__name__) 

@app.route('/hello', methods=['GET']) 
def helloworld(): 
	if(request.method == 'GET'): 
		session = SQL.base.Session()
		t = InvestmentConfig.getInvestmentIDs(session)
		session.close()
		data = {"data": t} 
		return jsonify(data) 


if __name__ == '__main__': 
	app.run(debug=True,host='0.0.0.0') 
