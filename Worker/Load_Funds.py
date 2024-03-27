
from Processing.Price import Price
from Processing.FundConfig import FundConfig


funds = FundConfig.importJSONconfig("/home/stanislawhorna/VScode/Investment/Worker/Funds.json")

FundConfig.insertFundConfig(funds)


Price.updateQuotation()







