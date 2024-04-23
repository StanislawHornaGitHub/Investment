"""
.DESCRIPTION
    SQLAlchemy Base file to init the connection with PostgreSQL DB
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      24-Mar-2024
    ChangeLog:

    Date            Who                     What

"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

IP = os.getenv('DB_IP_Address', 'localhost')
PORT  = os.getenv('DB_Port', '5432')
USERNAME = os.getenv('DB_Username', 'api_write')
PASSWORD = os.getenv('DB_Password', 'inv!w_ap_ite2')
DB_NAME = os.getenv('DB_Name', 'Investments')

connectionString = f"postgresql://{USERNAME}:{PASSWORD}@{IP}:{PORT}/{DB_NAME}"

engine = create_engine(connectionString)
Session = sessionmaker(bind=engine)

Base = declarative_base()