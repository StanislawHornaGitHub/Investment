"""
.DESCRIPTION
    Definition file for session as write user.
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      05-May-2024
    ChangeLog:

    Date            Who                     What

"""

import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

IP = os.getenv('DB_IP_Address', 'localhost')
PORT = os.getenv('DB_Port', '5432')
DB_NAME = os.getenv('DB_Name', 'Investments')
USERNAME = os.getenv('DB_Username_rw', 'api_write')
PASSWORD = os.getenv('DB_Password_rw', 'inv!w_ap_ite2')

connectionString = f"postgresql://{USERNAME}:{PASSWORD}@{IP}:{PORT}/{DB_NAME}"

engine = create_engine(connectionString)
Session_rw = sessionmaker(bind=engine)
