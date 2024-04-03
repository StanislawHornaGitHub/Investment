### DESCRIPTION
# Docker file to create Docker image for Investments API.

### INPUTS
# TZ - Desired timezone
# DB_IP_Address - IP address of PostgreSQL engine.
# DB_Port - Communication port for PostgreSQL engine.
# DB_Username - Username to connect to  Database.
# DB_Password - Password to connect to  Database.
# DB_Name - Investments Database name.
# FLASK_DEBUG - [True/False] value for debug mode.

### CHANGE LOG
# Author:   Stanisław Horna
# GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
# Created:  29-Mar-2024
# Version:  1.1

# Date            Who                     What
# 2024-04-03      Stanisław Horna         Timezone config added.

FROM ubuntu:latest

# Install Python and pip
RUN apt update
RUN apt install -y python3-dev 
RUN apt install -y pip

# Set timezone
ENV TZ="Europe/Warsaw"
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata

# Set working directory and copy required files
WORKDIR /App
COPY . /App

# Install Python packages
RUN pip install --upgrade pip
RUN pip install python-dateutil
RUN pip install requests
RUN pip install flask
RUN pip install psycopg2-binary
RUN pip install SQLAlchemy

# Set environmental variables

# PostgreSQL variables
ENV DB_IP_Address="192.168.0.212"
ENV DB_Port="5532"
ENV DB_Username="Invest_SH"
ENV DB_Password="DefP4550RD"
ENV DB_Name="Investments"

# Flask variables
ENV FLASK_DEBUG="True"

# Start API program
CMD ["python3", "./Investment_API.py"]