"""
.DESCRIPTION
    SQLAlchemy ORM file to define funds view.
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      24-Mar-2024
    ChangeLog:

    Date            Who                     What

"""

from sqlalchemy import Column, String, Integer, Float, DateTime

from SQL.base import Base


class Fund(Base):
    __tablename__ = 'funds'

    fund_id = Column(Integer, primary_key=True, autoincrement=True)
    fund_name = Column(String)
    category_name = Column(String)
    category_short = Column(String)
    fund_url = Column(String)

    def __init__(self, fund_url):
        self.fund_id = fund_url.split('/')[4]
        self.fund_name = fund_url.split('/')[5].replace('-', ' ').title()
        self.category_name = fund_url.split('/')[3].replace('-', ' ').title()
        categoryName = fund_url.split('/')[3]
        self.category_short = ''.join(
            [word[0] for word in categoryName.split("-")]
        )
        self.fund_url = fund_url
        
    
    def getFundID(self) -> str:
        return self.fund_id
    
    def getFundCategoryShort(self) -> str:
        return self.category_short