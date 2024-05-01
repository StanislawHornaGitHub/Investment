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
# Version:  1.2

# Date            Who                     What
# 2024-04-03      Stanisław Horna         Timezone config added.
#
# 2024-04-24      Stanisław Horna         Ubuntu latest changed to static one (22.04)
#                                         WSGI dependencies instalation added. Startup CMD changed.
#
# 2024-04-30      Stanisław Horna         Add environmental variable for log level.
#

FROM ubuntu:22.04

# Install Python and pip
RUN apt update
RUN apt install -y python3-dev
RUN apt install -y pip
RUN apt install -y gcc libpcre3-dev libpcre3

# Set timezone
ENV TZ="Europe/Warsaw"
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata

# Set working directory and copy required files
WORKDIR /App
COPY . /App

# Install Python packages
RUN pip install -r requirements.txt

# Set environmental variables

# PostgreSQL variables
ENV DB_IP_Address="PGDB"
ENV DB_Port="5432"
ENV DB_Username="api_write"
ENV DB_Password="inv!w_ap_ite2"
ENV DB_Name="Investments"
ENV LOG_LEVEL="DEBUG"
ENV LOKI_IP_Address="Loki"
ENV LOKI_PORT="3100"

# Flask variables
ENV FLASK_DEBUG="True"

# Start API program
CMD ["uwsgi", "--ini", "./wsgi.ini"]