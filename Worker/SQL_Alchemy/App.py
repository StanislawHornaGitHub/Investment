from base import Session
from Tables import *
import datetime
from dateutil.parser import parse

session = Session()

fund = session.query(Funds).all()
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

    session.add(quot)


session.commit()
session.close()