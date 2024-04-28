### DESCRIPTION
# Docker file to create Docker image for Checker service.
# It will be responsivle for checking if there are new quotations available
# and invoking the download automatically.

### INPUTS


### CHANGE LOG
# Author:   Stanisław Horna
# GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
# Created:  24-Apr-2024
# Version:  1.0

# Date            Who                     What

FROM ubuntu:22.04

# Install Python and pip
RUN apt update
RUN apt install -y python3-dev
RUN apt install -y pip

# Set working directory and copy required files
WORKDIR /App
COPY . /App

# Install Python packages
RUN pip install -r requirements.txt

# Set environmental variables
ENV FLASK_IP_Address="API"
ENV FLASK_Port="5000"

# Start program ("-u" param is required to see print output in docker logs)
CMD ["python3", "-u", "./Checker.py"]