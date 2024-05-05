import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

IP = os.getenv('DB_IP_Address', 'localhost')
PORT = os.getenv('DB_Port', '5432')
USERNAME = os.getenv('DB_Username', 'api_write')
PASSWORD = os.getenv('DB_Password', 'inv!w_ap_ite2')
DB_NAME = os.getenv('DB_Name', 'Investments')

connectionString = f"postgresql://{USERNAME}:{PASSWORD}@{IP}:{PORT}/{DB_NAME}"

engine = create_engine(connectionString)
Session_rw = sessionmaker(bind=engine)
