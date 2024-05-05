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

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
