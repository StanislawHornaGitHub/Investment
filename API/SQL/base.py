import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

IP = os.getenv('DB_IP_Address', 'localhost')
PORT  = os.getenv('DB_Port', '5532')
USERNAME = os.getenv('DB_Username', 'Invest_SH')
PASSWORD = os.getenv('DB_Password', 'DefP4550RD')
DB_NAME = os.getenv('DB_Name', 'Investments')

connectionString = f"postgresql://{USERNAME}:{PASSWORD}@{IP}:{PORT}/{DB_NAME}"

engine = create_engine(connectionString)
Session = sessionmaker(bind=engine)

Base = declarative_base()