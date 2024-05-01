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

FROM alpine:3.19

# Install Python and pip
RUN apk update
RUN apk add curl


# Set working directory and copy required files
WORKDIR /DataImport
COPY . /DataImport


# Set environmental variables

# Flask environment variables
ENV FLASK_IP_Address="API"
ENV FLASK_PORT="5000"


# Start API program
CMD ["sh", "InsertData.sh"]