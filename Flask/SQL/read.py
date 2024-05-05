"""
.DESCRIPTION
    Definition file for session as read-only user.
    

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
USERNAME = os.getenv('DB_Username_ro', 'api_read')
PASSWORD = os.getenv('DB_Password_ro', 'inv!r_ap_ead1')

connectionString = f"postgresql://{USERNAME}:{PASSWORD}@{IP}:{PORT}/{DB_NAME}"

engine = create_engine(connectionString)
Session_ro = sessionmaker(bind=engine)
