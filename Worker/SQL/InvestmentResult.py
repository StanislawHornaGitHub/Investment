from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey

from SQL.base import Base


class InvestmentResult(Base):
    __tablename__ = 'investment_results'

    result_date = Column(DateTime, primary_key=True)
    fund_id = Column(String, primary_key=True)
    investment_id = Column(Integer, primary_key=True)
    fund_participation_units = Column(Float)
    fund_invested_money = Column(Float)
    fund_value = Column(Float)
    last_day_result = Column(Float)
    last_week_result = Column(Float)
    last_month_result = Column(Float)
    last_year_result = Column(Float)
    

    def __init__(
        self,
        result_date,
        fund_id,
        investment_id,
        fund_participation_units,
        fund_invested_money,
        fund_value,
        last_day_result=None,
        last_week_result=None,
        last_month_result=None,
        last_year_result=None
    ):
        self.result_date = result_date
        self.fund_id = fund_id
        self.investment_id = investment_id
        self.fund_participation_units = fund_participation_units
        self.fund_invested_money = fund_invested_money
        self.fund_value = fund_value
        self.last_day_result = last_day_result
        self.last_week_result = last_week_result
        self.last_month_result = last_month_result
        self.last_year_result = last_year_result

    @staticmethod
    def getInvestmentResult(investment_id: int, session):
        output = (
            session
            .query(
                InvestmentResult.result_date,
                InvestmentResult.fund_id,
                InvestmentResult.investment_id,
                InvestmentResult.fund_participation_units,
                InvestmentResult.fund_invested_money,
                InvestmentResult.fund_value
                )
            .filter(InvestmentResult.investment_id == investment_id)
            .order_by(InvestmentResult.result_date.asc())
            .all()
        )
        result = []
        for date, fund, investment, units, money, value in output:
            result.append(
                {
                    "result_date": date,
                    "investment_id": investment,
                    "fund_id": fund,
                    "fund_participation_units": units,
                    "fund_invested_money": money,
                    "fund_value": value
                }
            )
        
        return result