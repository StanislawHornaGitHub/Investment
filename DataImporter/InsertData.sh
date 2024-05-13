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
# Version:  1.3

# Date            Who                     What
# 2024-05-01      Stanisław Horna         Set API ip and port from environment variables.
#                                         Add silent flag to curl.
#
# 2024-05-04      Stanisław Horna         Add removing backslashes from message to log.
#
# 2024-05-13      Stanisław Horna         Add directory for config files to import.
#

API_IP_ADDRESS=$FLASK_IP_Address
API_PORT=$FLASK_PORT

CONFIG_DIRECTORY="./Configs"
FUNDS_FILE="Funds.json"
INVESTMENT_FILES_SUFFIX="_Investments.json"

Main() {
    logMessage "Main" "Script started" "info"
    importFundsConfig
    importInvestmentConfig
    logMessage "Main" "Script completed" "info"
}

importFundsConfig() {
    logMessage "importFundsConfig" "Inserting funds" "info"

    # Read JSON file with funds
    jsonFunds=$(cat "$CONFIG_DIRECTORY/$FUNDS_FILE") || exit 1

    logMessage "importFundsConfig" "Funds config file read" "info"

    # Invoke PUT /FundConfig method
    response=$(
        curl --silent --location --request PUT "$API_IP_ADDRESS:$API_PORT/FundConfig" \
            --header 'Content-Type: application/json' \
            --data "$jsonFunds"
    )
    logMessage "importFundsConfig" "API response: $response" "debug"
    logMessage "importFundsConfig" "Funds config import completed" "info"
}

importInvestmentConfig() {
    logMessage "importInvestmentConfig" "Inserting investments config" "info"

    for filename in "$CONFIG_DIRECTORY"/*"$INVESTMENT_FILES_SUFFIX"; do

        # Read JSON file with investment details
        jsonInvestment=$(cat "$filename")
        logMessage "importInvestmentConfig" "File $filename read" "info"

        # Invoke PUT /InvestmentConfig method
        response=$(
            curl --silent --location --request PUT "$API_IP_ADDRESS:$API_PORT/InvestmentConfig" \
                --header 'Content-Type: application/json' \
                --data "$jsonInvestment"
        )
        logMessage "importInvestmentConfig" "API response: $response" "debug"
    done

    logMessage "importInvestmentConfig" "Investment config import completed" "info"
}

logMessage() {
    function=$1
    message=$2
    level=$3
    timestamp=$(date +"%Y-%m-%d %H:%M:%S.%6N")

    # replace new lines with spaces
    message="$(echo "$message" | tr '\n' ' ')"
    # replace backslashes
    message="$(echo "$message" | tr -d '\\')"
    # replace double quotes with single quotes
    message="$(echo "$message" | tr '"' "'")"
    # replace several spaces with just one
    message=$(echo "$message" | tr -s ' ')

    level="$(echo "$level" | tr '[:lower:]' '[:upper:]')"
    {
        echo -n "{"
        echo -n "\"timestamp\" : \"$timestamp\", "
        echo -n "\"level\" : \"$level\", "
        echo -n "\"funcName\" : \"$function\", "
        echo -n "\"message\" : \"$message\""
        echo "}"
    } >>"$LOG_PATH$LOG_FILE_NAME.json"

}

Main
