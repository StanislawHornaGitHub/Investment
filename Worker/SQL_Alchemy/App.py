from base import Session
from Tables import *
import datetime
from dateutil.parser import parse
from sqlalchemy import select
session = Session()

fund = session.query(Funds).where(Funds.fund_id == "ING43")
print(select(Funds).where(Funds.fund_id == "ING43"))
print(fund[0].fund_name)
date = parse('2023-01-10')
for i in range(1, 11):
    quot = Quotations(
        parse(f"2023-02-{i}"),
        fund[0].fund_id,
        123,
        0.1,
        0.2,
        0.3,
        0.4
        )

    #session.add(quot)


#session.commit()
session.close()