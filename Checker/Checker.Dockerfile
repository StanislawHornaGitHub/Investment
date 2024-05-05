### DESCRIPTION
# Docker file to create Docker image for Checker service.
# It will be responsible for checking if there are new quotations available
# and invoking the download automatically.

### INPUTS


### CHANGE LOG
# Author:   Stanisław Horna
# GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
# Created:  24-Apr-2024
# Version:  1.2

# Date            Who                     What
# 2024-04-29      Stanisław Horna         Add environmental variable for log level.
#
# 2024-05-03      Stanisław Horna         Add logs directory at root.
#                                         Implement log related environmental variables.
#

FROM ubuntu:22.04

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
RUN pip install -r requirements.txt

RUN mkdir /log
RUN chmod 777 /log

# Set environmental variables
ENV FLASK_IP_Address="API"
ENV FLASK_Port="5000"

ENV LOKI_IP_Address="Loki"
ENV LOKI_PORT="3100"

ENV LOG_LEVEL="DEBUG"
ENV LOG_TYPE="JSON"
ENV LOG_PATH="/log/"
ENV LOG_FILE_NAME="Checker"


# Start program ("-u" param is required to see print output in docker logs)
CMD ["python3", "-u", "./Checker.py"]