#!/bin/sh

### DESCRIPTION
# Deploy Investment system
# Covered Tasks:
#   1. Deploy PostgreSQL container
#   2. Deploy Flask API container
#   3. Insert init data to the system

### INPUTS
# API_IP_ADDRESS - IP address of Flask API
# API_PORT - Flask API port
# FUNDS_FILE - Name of funds file
# INVESTMENT_FILES_SUFFIX - suffix

### OUTPUTS
# Logs

### EXIT CODES
# 0 - Success
# 1 - Failed to change directory
# 2 - Container deployment script failed
# 3 - Data insert script failed
# 4 -

### CHANGE LOG
# Author:   Stanisław Horna
# GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
# Created:  27-Mar-2024
# Version:  1.0

# Date            Who                     What

POSTGRESQL_DIR="./PostgreSQL"
API_DIR="./API"
DATA_IMPORT_DIR="./InitialDataImport"

API_IP_ADDRESS="192.168.0.212"
API_PORT="5000"

Main() {
    StartPostgresContainer
    StartFlaskContainer
    LoadFundsAndInvestments
    DownloadFundQuotation
    CalculateInvestmentResults
}

StartPostgresContainer() {

    # Set postgres directory,
    # because in the startup script invokes docker build is using current directory
    cd "$POSTGRESQL_DIR" || exit 1

    # Start script to build docker image and start container
    ExecuteStartupScript

    # Go back to root directory
    SetRootDirectory
}

StartFlaskContainer() {

    # Set API directory,
    # because in the startup script invokes docker build is using current directory
    cd "$API_DIR" || exit 1

    # Start script to build docker image and start container
    ExecuteStartupScript

    # Go back to root directory
    SetRootDirectory
}

LoadFundsAndInvestments() {

    # Set InitialDataImport directory,
    # because script is looking for particular JSON files within same directory
    cd "$DATA_IMPORT_DIR" || exit 1

    # Start script which will invoke appropriate API calls
    ./InsertData.sh || exit 3

    # Go back to root directory
    SetRootDirectory
}

DownloadFundQuotation() {
    curl --location --request PUT "$API_IP_ADDRESS:$API_PORT/FundQuotation" \
        --header 'Content-Type: application/json'
}

CalculateInvestmentResults() {
    curl --location --request PUT "$API_IP_ADDRESS:$API_PORT/InvestmentRefund" \
        --header 'Content-Type: application/json'
}

ExecuteStartupScript() {

    ./rebuild.sh || exit 2
}

SetRootDirectory() {

    # Go back to root directory
    cd "$(git rev-parse --show-toplevel)" || exit 1
}

Main
