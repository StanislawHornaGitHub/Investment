from Processing.InvestmentConfig import InvestmentConfig



invest = InvestmentConfig.importJSONconfig('/home/stanislawhorna/VScode/Investment/Worker/Investments.json')

InvestmentConfig.insertInvestmentConfig(invest, "Stan")
