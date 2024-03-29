from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://Invest_SH:DefP4550RD@localhost:5532/Investments')
Session = sessionmaker(bind=engine)

Base = declarative_base()