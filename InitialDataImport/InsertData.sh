#!/bin/sh

### DESCRIPTION
# Script to insert data to newly deployed system

### INPUTS
# API_IP_ADDRESS - IP address of Flask API
# API_PORT - Flask API port
# FUNDS_FILE - Name of funds file
# INVESTMENT_FILES_SUFFIX - suffix

### OUTPUTS
#

### EXIT CODES
#

### CHANGE LOG
# Author:   Stanisław Horna
# GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
# Created:  31-Mar-2024
# Version:  1.0

# Date            Who                     What

API_IP_ADDRESS="192.168.0.212"
API_PORT="5000"

FUNDS_FILE="Funds.json"
INVESTMENT_FILES_SUFFIX="_Investments.json"

Main() {

    importFundsConfig
    importInvestmentConfig
}

importFundsConfig() {

    # Read JSON file with funds
    jsonFunds=$(cat "./$FUNDS_FILE")

    # Invoke PUT /FundConfig method
    curl --location --request PUT "$API_IP_ADDRESS:$API_PORT/FundConfig" \
        --header 'Content-Type: application/json' \
        --data "$jsonFunds"
}

importInvestmentConfig() {
    for filename in ./*"$INVESTMENT_FILES_SUFFIX"; do

        # Read JSON file with investment details
        jsonInvestment=$(cat "$filename")

        # Invoke PUT /InvestmentConfig method
        curl --location --request PUT "$API_IP_ADDRESS:$API_PORT/InvestmentConfig" \
            --header 'Content-Type: application/json' \
            --data "$jsonInvestment" >/dev/null
    done
}

Main
