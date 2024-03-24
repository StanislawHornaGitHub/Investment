from sqlalchemy import Column, String, Integer, Float, DateTime

from base import Base


class Funds(Base):
    __tablename__ = 'funds'

    fund_id = Column(Integer, primary_key=True)
    fund_name = Column(String)
    category_name = Column(String)
    fund_url = Column(String)

    def __init__(self, fund_id, fund_name, category_name, fund_url):
        self.fund_id = fund_id
        self.fund_name = fund_name
        self.category_name = category_name
        self.fund_url = fund_url


class Quotations(Base):
    __tablename__ = 'quotations'

    date = Column(DateTime, primary_key=True)
    fund_id = Column(String, primary_key=True)
    value = Column(Float)
    daily_change = Column(Float)
    weekly_change = Column(Float)
    monthly_change = Column(Float)
    yearly_change = Column(Float)

    def __init__(self, q_date, fund_id, value, daily_change, weekly_change,monthly_change,yearly_change):
        self.date = q_date
        self.fund_id = fund_id
        self.value = value
        self.daily_change = daily_change
        self.weekly_change = weekly_change
        self.monthly_change = monthly_change
        self.yearly_change = yearly_change