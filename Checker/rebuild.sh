#!/bin/sh

### DESCRIPTION
# Script to build fresh image of Checker service,
# run docker container.

### INPUTS
# None

### OUTPUTS
#  1.  Docker build image
# (2). Docker logs if docker run failed

### EXIT CODES
# 0 - Success
# 1 - Docker daemon is not running
# 2 - Image build failed
# 3 - Container did not start correctly

### CHANGE LOG
# Author:   Stanisław Horna
# GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
# Created:  05-May-2024
# Version:  1.0

# Date            Who                     What
#

# define echo colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
RESET='\033[0m'

# define docker variables
DockerImageName="investment/checker"
DockerfileName="Checker.Dockerfile"
DockerContainerName="Investment_Checker"

Main() {

    # check if docker is running
    if docker ps -a -q -f name="Certainly Not Exist"; then
        printGreenMessage "Docker daemon is running"
    else
        printRedMessage "Docker daemon is not running"
        exit 1
    fi

    # check if postgreSQL container is running, if yes remove it.
    if [ -n "$(docker ps -a -q -f name="$DockerContainerName")" ]; then
        docker rm -f -v $DockerContainerName
        printGreenMessage "Old Container removed"
    else
        printYellowMessage "Container was not running"
    fi

    # build new image for DB container
    if docker build -t $DockerImageName -f $DockerfileName .; then
        printGreenMessage "Image build successful"
    else
        printRedMessage "Image build failed"

        exit 2
    fi

    # run container based on the new docker image
    docker run --name $DockerContainerName -d $DockerImageName

    # invoke sleep to wait for full initialization of the database
    waitForContainerInit
    printGreenMessage "Container is running"

    exit 0
}

waitForContainerInit() {

    # init variable
    numOfDBstartups=0

    # loop until SQL engine perform 2 complete startups,
    # each startup is announced by log message "database system is ready to accept connections"
    # after first one Database is initialized from scripts located in "SQL" directory,
    # once DB init is completed, another restart is performed and container is ready to work.
    while [ "$numOfDBstartups" -le 0 ]; do

        sleep 0.1
        # check if container is still running,
        #   if not display container logs.
        #   if yes invoke DB tests.

        # if there were some error during initialization container will not be running
        if [ -z "$(docker ps -q -f name="$DockerContainerName")" ]; then
            docker logs $DockerContainerName

            printRedMessage "Container is not running"
            exit 3
        fi
        numOfDBstartups=$(docker logs $DockerContainerName 2>&1 | grep -c " - INFO - Checker - Service started$")
    done
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
