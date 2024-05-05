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
# Version:  1.5

# Date            Who                     What
# 2024-04-03      Stanisław Horna         Timezone config added.
#
# 2024-04-24      Stanisław Horna         Ubuntu latest changed to static one (22.04)
#                                         WSGI dependencies instalation added. Startup CMD changed.
#
# 2024-04-30      Stanisław Horna         Add environmental variable for log level.
#
# 2024-05-03      Stanisław Horna         Add logs directory at root.
#                                         Implement log related environmental variables.
#
# 2024-05-05      Stanisław Horna         Separate DB read and write users.
#

FROM ubuntu:22.04

# Install Python and pip
RUN apt update
RUN apt install -y python3-dev
RUN apt install -y pip
RUN apt install -y gcc libpcre3-dev libpcre3
RUN apt install -y curl

# Set timezone
ENV TZ="Europe/Warsaw"
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata

# Set working directory and copy required files
WORKDIR /App
COPY . /App

# Install Python packages
RUN pip install -r requirements.txt

RUN mkdir /log
RUN chmod 777 /log

# Set environmental variables

# PostgreSQL variables
ENV DB_IP_Address="PGDB"
ENV DB_Port="5432"
ENV DB_Name="Investments"
ENV DB_Username_rw="api_write"
ENV DB_Password_rw="inv!w_ap_ite2"
ENV DB_Username_ro="api_read"
ENV DB_Password_ro="inv!r_ap_ead1"

ENV LOKI_IP_Address="Loki"
ENV LOKI_PORT="3100"

ENV LOG_LEVEL="DEBUG"
ENV LOG_TYPE="JSON"
ENV LOG_PATH="/log/"
ENV LOG_FILE_NAME="Flask"

# Flask variables
ENV FLASK_DEBUG="True"

# Start API program
CMD ["uwsgi", "--ini", "./wsgi.ini"]