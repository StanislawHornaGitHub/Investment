### DESCRIPTION
# Docker file to create Docker image start-up data importer.

### INPUTS
# None

### CHANGE LOG
# Author:   Stanisław Horna
# GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
# Created:  1-May-2024
# Version:  1.0

# Date            Who                     What
#

FROM ubuntu:22.04

RUN apt update
RUN apt install -y curl

# Set working directory and copy required files
WORKDIR /DataImport
COPY ./InsertData.sh /DataImport/InsertData.sh

# Set timezone
ENV TZ="Europe/Warsaw"
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata

RUN mkdir /log
RUN chmod 777 /log


# Set environmental variables

# Flask environment variables
ENV FLASK_IP_Address="API"
ENV FLASK_PORT="5000"

ENV LOG_PATH="/log/"
ENV LOG_FILE_NAME="DataImporter"


# Start program
CMD ["sh", "InsertData.sh"]