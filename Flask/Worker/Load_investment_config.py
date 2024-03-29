from Processing.InvestmentConfig import InvestmentConfig



invest = InvestmentConfig.importJSONconfig('/home/stanislawhorna/VScode/Investment/Flask/Worker/Investments.json')

InvestmentConfig.insertInvestmentConfig(invest, "Stan")
