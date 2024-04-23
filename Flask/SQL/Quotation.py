"""
.DESCRIPTION
    SQLAlchemy ORM file to define quotations view.
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      24-Mar-2024
    ChangeLog:

    Date            Who                     What

"""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey

from SQL.base import Base

class Quotation(Base):
    __tablename__ = 'quotations'

    date = Column(DateTime, primary_key=True)
    fund_id = Column(Integer, ForeignKey("funds.fund_id"), primary_key=True)
    value = Column(Float)
    daily_change = Column(Float)
    weekly_change = Column(Float)
    monthly_change = Column(Float)
    yearly_change = Column(Float)

    def __init__(self, q_date, fund_id, value, daily_change=None, weekly_change=None, monthly_change=None, yearly_change=None):
        self.date = q_date
        self.fund_id = fund_id
        self.value = value
        self.daily_change = daily_change
        self.weekly_change = weekly_change
        self.monthly_change = monthly_change
        self.yearly_change = yearly_change
        
    def downloadNewQuotation(self):
        pass