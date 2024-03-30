from Processing.InvestmentConfig import InvestmentConfig



invest = InvestmentConfig.importJSONconfig('/home/stanislawhorna/VScode/Investment/API/json/Investments.json')

InvestmentConfig.insertInvestmentConfig(invest, "Stan")
