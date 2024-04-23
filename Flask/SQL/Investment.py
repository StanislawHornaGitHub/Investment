"""
.DESCRIPTION
    SQLAlchemy ORM file to define investments view.
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      25-Mar-2024
    ChangeLog:

    Date            Who                     What

"""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey

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
