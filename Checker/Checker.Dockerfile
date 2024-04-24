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