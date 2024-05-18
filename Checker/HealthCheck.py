"""
.DESCRIPTION
    Script to check if Checker service is up and running.
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      18-May-2024
    ChangeLog:

    Date            Who                     What

"""
import os
import yaml
import datetime
from Log.Logger import logger

DEFAULT_STATUS_FILE_PATH = '/var/lib/checker/status.yaml'
HEARTBEAT_KEY = 'Heartbeat'


def Main():

    # if service is healthy exit with 0
    if isCheckerHealthy():
        exit(0)
    else:
        # otherwise log an error message and exit with 1
        logger.error("Service unhealthy")
        exit(1)


def isCheckerHealthy() -> bool:

    # get time interval of how often status file is refreshed
    configCheckInterval = (
        int(
            os.getenv(
                'CONFIG_CHECK_INTERVAL_MS',
                60000
            )
        )
        / 1000
    )

    # calculate 30% error, to avoid misleading unhealthy notifications
    errorThreshold = configCheckInterval * 0.3

    # get heartbeat timestamp from status file
    lastHeartBeat = getLastHeartBeatDate()

    # calculate time difference
    timeDiff = (
        (datetime.datetime.now() - lastHeartBeat)
        .seconds
    )

    # check if time difference is less than status file refresh period + threshold for error
    # other words, check if heartbeat is not older than set config check interval
    return timeDiff < (configCheckInterval + errorThreshold)


def getLastHeartBeatDate() -> datetime.datetime:

    # extract from dict result heartbeat key value,
    # if value is not available return 1900-01-01
    return (
        readStatusFile()
        .get(
            HEARTBEAT_KEY,
            datetime.datetime(1900, 1, 1)
        )
    )


def readStatusFile() -> dict[str, datetime.datetime | list[datetime.datetime]]:

    # get path to file from environmental variables
    statusFilePath = os.getenv(
        'STATUS_FILE_PATH',
        DEFAULT_STATUS_FILE_PATH
    )

    # check if file exists
    if os.path.exists(statusFilePath):
        try:

            # open file, read YAML structure and return it
            with open(statusFilePath, 'r') as yaml_file:
                data = yaml.safe_load(yaml_file)
                return data
        except:

            # if there was an error in reading or loading return empty dict
            return {}
    else:

        # if file do not exist return empty dict
        return {}


if __name__ == '__main__':
    Main()
