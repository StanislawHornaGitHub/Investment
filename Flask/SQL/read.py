import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

IP = os.getenv('DB_IP_Address', 'localhost')
PORT = os.getenv('DB_Port', '5532')
USERNAME = os.getenv('DB_Username', 'api_read')
PASSWORD = os.getenv('DB_Password', 'inv!r_ap_ead1')
DB_NAME = os.getenv('DB_Name', 'Investments')

connectionString = f"postgresql://{USERNAME}:{PASSWORD}@{IP}:{PORT}/{DB_NAME}"

engine = create_engine(connectionString)
Session_ro = sessionmaker(bind=engine)
