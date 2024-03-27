
from Processing.InvestmentCalcResult import InvestmentCalcResult
from Processing.InvestmentConfig import InvestmentConfig
import SQL

session = SQL.base.Session()

investmentsToRefresh = InvestmentConfig.getInvestmentIDs(session)

for id in investmentsToRefresh:
    InvestmentCalcResult.calculateResult(id)