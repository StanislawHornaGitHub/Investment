### DESCRIPTION
# Docker file to create Docker image for Investments DB, with python functions support.

### INPUTS
# POSTGRES_DB - Database name (do not change)
# POSTGRES_PASSWORD - Super admin password
# POSTGRES_USER - Super admin username

### CHANGE LOG
# Author:   Stanisław Horna
# GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
# Created:  24-Mar-2024
# Version:  1.0

# Date            Who                     What

FROM postgres:16.2

# Install plpython extension for code written in Python support
RUN apt-get update
RUN apt-get install -y postgresql-plpython3-16
RUN apt-get install -y locales locales-all

# Set timezone
ENV TZ="Europe/Warsaw"
RUN date

# Set DB name and default user
ENV POSTGRES_DB="Investments"
ENV POSTGRES_PASSWORD="DefP4550RD"
ENV POSTGRES_USER="Invest_SH"

# Set DB collate
ENV POSTGRES_INITDB_ARGS="--encoding=UTF-8 --lc-collate=pl_PL.utf8 --lc-ctype=pl_PL.utf8"

# Copy scripts to run on startup
COPY ./SQL/* /docker-entrypoint-initdb.d/

EXPOSE 5432
CMD ["postgres"]
