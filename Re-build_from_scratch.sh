#!/bin/sh

### DESCRIPTION
# Script to deploy Investment system or rebuild.
# Rebuilding covers deleting all persistant DB storage, and forces complete compose re-creation.
# Covered Tasks:
#   1. Stop currently running compose
#   2. Remove persistant storage
#   3. Build docker images
#   4. Start docker compose
#   5. Import initial config for funds and investments
#   6. Download fund quotation from Internet
#   7. Calculate investment result

### INPUTS
# None - all variables are read out from .env file

### OUTPUTS
# None

### EXIT CODES
#  0 - Success
#  1 - Docker daemon is not running
#  2 - Failed to change directory
#  3 - Failed to read .env file
# 10 - PostgreSQL container initialization failed

### CHANGE LOG
# Author:   Stanisław Horna
# GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
# Created:  23-Apr-2024
# Version:  1.3

# Date            Who                     What
# 2024-04-28      Stanisław Horna         Remove downloading quotations and refund calculation,
#                                         due to implementation of Checker service,
#                                         which will automatically perform those operations.
#
# 2024-05-01      Stanisław Horna         Remove initial data import as it was moved to separate container.
#
# 2024-05-04      Stanisław Horna         Add prompt for user about removing persistent data.
#

# define echo colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
RESET='\033[0m'

Main() {
    askUserAboutStorageRemoval
    checkDockerDaemonRunning
    stopRunningContainers
    removePersistantStorage
    buildCompose
    startCompose
    #waitForPostgreSpinUp
    showComposeStatus
}

checkDockerDaemonRunning() {

    # check if docker is running
    if docker ps -a -q -f name="Certainly Not Exist"; then
        printGreenMessage "Docker daemon is running"
    else
        printRedMessage "Docker daemon is not running"
        exit 1
    fi
}

stopRunningContainers() {

    docker compose down
}

askUserAboutStorageRemoval() {

    response=""
    while [ "$response" != "y" ] && [ "$response" != "n" ]; do
        echo "Remove persistent data? [y/n]: \c"
        read -r response
    done
}

removePersistantStorage() {

    if [ "$response" = "y" ]; then
        printYellowMessage "Removing persistant storage"

        dirPath=$(getDotenvVariable "APP_DATA_PATH")
        sudo rm -fr "$dirPath"

        dirPath=$(getDotenvVariable "APP_LOG_PATH")
        sudo rm -fr "$dirPath"
    fi
}

buildCompose() {

    printYellowMessage "Building compose containers"

    docker compose build
}

startCompose() {

    printYellowMessage "Starting compose containers"

    docker compose up -d --force-recreate
}

waitForPostgreSpinUp() {

    PGcontainerName=$(getDotenvVariable "POSTGRESQL_CONTAINER_NAME")
    waitForContainerInit "$PGcontainerName" "database system is ready to accept connections$" 2 10
}

showComposeStatus() {

    docker compose ps
}

waitForContainerInit() {
    DockerContainerName=$1
    PhraseToLookFor=$2
    PhraseOccurences=$3
    ExitCode=$4

    # init variable
    numOfDBstartups=0

    # loop until SQL engine perform 2 complete startups,
    # each startup is announced by log message "database system is ready to accept connections"
    # after first one Database is initialized from scripts located in "SQL" directory,
    # once DB init is completed, another restart is performed and container is ready to work.
    while [ "$numOfDBstartups" -lt "$PhraseOccurences" ]; do

        sleep 0.1
        # check if container is still running,
        #   if not display container logs.
        #   if yes invoke DB tests.

        # if there were some error during initialization container will not be running
        if [ -z "$(docker ps -q -f name="$DockerContainerName")" ]; then
            docker logs "$DockerContainerName"

            printRedMessage "Container is not running"
            exit "$ExitCode"
        fi
        numOfDBstartups=$(docker logs "$DockerContainerName" 2>&1 | grep -c "$PhraseToLookFor")
    done

    printGreenMessage "$DockerContainerName has started"
}

getDotenvVariable() {
    VariableName=$1

    # Check if .env file exist
    if [ -e .env ]; then

        # grep variable name from .env file
        # split it by = and print second element
        # sed to remove spaces before any char and after the latest one
        grep "$VariableName" .env | awk -F= '{print $2}' | sed 's/^[   ]*//;s/[    ]*$//'
    else
        exit 3
    fi
}

SetRootDirectory() {

    # Go back to root directory
    cd "$(git rev-parse --show-toplevel)" || exit 2
}

printGreenMessage() {
    Message=$1

    echo ""
    echo "${GREEN}$Message${RESET}"
    echo ""
}

printRedMessage() {
    Message=$1

    echo ""
    echo "${RED}$Message${RESET}"
    echo ""
}

printYellowMessage() {
    Message=$1

    echo ""
    echo "${YELLOW}$Message${RESET}"
    echo ""
}

Main
