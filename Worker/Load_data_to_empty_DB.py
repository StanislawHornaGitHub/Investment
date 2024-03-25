
import SQL
import AnalizyPL
from AnalizyPL.API import AnalizyFund
from SQL.Fund import Fund
from SQL.Quotation import Quotation
import datetime
from dateutil.parser import parse
from sqlalchemy import select, insert
from sqlalchemy import exc, func
import json


from Processing import Price

session = SQL.base.Session()


FundsToAdd = [
    "https://www.analizy.pl/fundusze-inwestycyjne-otwarte/UNI32/generali-oszczednosciowy",
    "https://www.analizy.pl/fundusze-inwestycyjne-otwarte/DWS05/investor-oszczednosciowy",
    "https://www.analizy.pl/fundusze-inwestycyjne-otwarte/ING43/goldman-sachs-japonia",
    "https://www.analizy.pl/fundusze-inwestycyjne-otwarte/DWS20/investor-top-50-malych-i-srednich-spolek",
    "https://www.analizy.pl/fundusze-inwestycyjne-otwarte/PZU40/pzu-globalny-obligacji-korporacyjnych",
    "https://www.analizy.pl/fundusze-inwestycyjne-otwarte/PZU45/pzu-sejf",
    "https://www.analizy.pl/fundusze-inwestycyjne-otwarte/PZU79/pzu-obligacji-krotkoterminowych"
]

# for f in FundsToAdd:
#     try:
#         f = Fund(f)
#         session.add(f)
#         session.commit()
#     except:
#         print('error')


Price.Price.updateQuotation()




session.close()



