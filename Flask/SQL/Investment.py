"""
.DESCRIPTION
    SQLAlchemy ORM file to define investments view.
    

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      25-Mar-2024
    ChangeLog:

    Date            Who                     What
    2024-04-26      Stanisław Horna         checkInvestmentIDisValid to check if investment with provided ID exists.

"""

from sqlalchemy import orm, Column, String, Integer, Float, DateTime, ForeignKey, exists

from SQL.base import Base


class Investment(Base):
    __tablename__ = 'investments'


    investment_id = Column(Integer, primary_key=True, autoincrement=True)
    investment_name = Column(String)
    investment_owner_id = Column(Integer)
    investment_owner = Column(String)
    investment_fund_id = Column(String, primary_key=True)
    operation_quotation_date = Column(DateTime, primary_key=True)
    operation_date = Column(DateTime)
    operation_value = Column(Float)
    operation_currency = Column(String)

    def __init__(
        self,
        investment_id,
        investment_name,
        investment_owner_id,
        operation_value,
        investment_owner=None,
        investment_fund_id=None,
        operation_quotation_date=None,
        operation_date=None,
        operation_currency=None
    ):
        self.investment_id = investment_id
        self.investment_name = investment_name
        self.investment_owner_id = investment_owner_id
        self.investment_owner = investment_owner
        self.investment_fund_id = investment_fund_id
        self.operation_quotation_date = operation_quotation_date
        self.operation_date = operation_date
        self.operation_value = operation_value
        self.operation_currency = operation_currency

    def checkInvestmentIDisValid(id: int, session: orm.session.Session) -> bool:
        return session.query(exists().where(Investment.investment_id == id)).scalar()