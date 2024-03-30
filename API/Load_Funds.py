
from Processing.Price import Price
from Processing.FundConfig import FundConfig


funds = FundConfig.importJSONconfig("/home/stanislawhorna/VScode/Investment/API/json/Funds.json")

FundConfig.insertFundConfig(funds)


Price.updateQuotation()







