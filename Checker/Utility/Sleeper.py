"""
.DESCRIPTION
    Class to handle sleeping the process between operations.


.NOTES

    Version:            1.3
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      28-Apr-2024
    ChangeLog:

    Date            Who                     What
    2024-04-29      Stanisław Horna         Add check-in after completed sleep.
                                            Add logging capabilities.
                                            
    2024-05-15      Stanisław Horna         Add DataImporter implementation.
    
    2024-05-16      Stanisław Horna         Code documented.

"""

import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from DataImporter.DataImporter import DataImporter
from Status.StatusFile import StatusFile
from Utility.Terminator import Terminator
from Log.Logger import logger


@dataclass
class Sleeper:

    SleepTimeInterval_ms: int = field(init=True, default=3600000)
    StatusFileCheckInterval_ms: int = field(init=True, default=60000)
    __IMPORTER: DataImporter = field(init=False, default=DataImporter())
    __TERMINATOR: Terminator = field(init=False, default=Terminator())

    __LastCheckIn: datetime = field(init=False)
    __NextCheckIn: datetime = field(init=False)

    def __post_init__(self):

        # refresh last and next check in dates
        self.checkIn()

        # read status file
        statusFileContent = StatusFile.readFile()

        # import fund and investment configs to system
        self.__IMPORTER.putChangedConfigs(
            statusFileContent.get(
                StatusFile.LAST_MODIFY_DATES_LABEL,
                {}
            )
        )

        # update status file with new data
        StatusFile.writeFile(
            NextCheckInTime=self.__NextCheckIn,
            LastModifyDates=self.__IMPORTER.getLastModifyDatesFromCache()
        )

        logger.debug(
            "Sleeper initialized. Sleep interval: %d Status file check interval: %d",
            self.SleepTimeInterval_ms,
            self.StatusFileCheckInterval_ms
        )

    def __last_check_in(self):
        '''
            Method to set Last check in datetime to now
        '''
        # set last check in date to now
        self.__LastCheckIn = datetime.now()

    def __next_check_in(self):
        '''
            Method to update Next check in datetime based on set time interval
        '''
        # calculate next check in date based on last one and interval
        self.__NextCheckIn = (
            self.__LastCheckIn + timedelta(
                milliseconds=self.SleepTimeInterval_ms
            )
        )

    def __calculate_time_to_sleep(self) -> float:
        '''
            Method to calculate how much time system has to next check time.
        '''
        # calculate remaining time to next check in
        TimeToSleep = (
            (
                self.__NextCheckIn - datetime.now()
            )
            .total_seconds()
        )

        # refresh last and next check in dates
        self.checkIn()

        # update status file
        StatusFile.writeFile(
            NextCheckInTime=self.__NextCheckIn,
            LastModifyDates=self.__IMPORTER.getLastModifyDatesFromCache()
        )

        # return calculated time to sleep
        return TimeToSleep

    def __exit_sleep_loop(self) -> bool:
        '''
            Method to check if there were any updates to config files, which were inserted to system,
            or next check in time already passed and verification if new quotation exists is needed.
        '''
        # read status file
        statusFileContent = StatusFile.readFile()

        # import fund and investment configs to system
        configPutStatus = self.__IMPORTER.putChangedConfigs(
            statusFileContent.get(
                StatusFile.LAST_MODIFY_DATES_LABEL,
                {}
            )
        )

        # extract next check in time from status file
        sleeperCheckInFromStatusFile: datetime = statusFileContent.get(
            StatusFile.NEXT_CHECK_IN_LABEL,
            {}
        )

        # check if any config was inserted to system
        if configPutStatus is True:

            logger.debug("Config change found")
            # refresh last and next check in dates
            self.checkIn()

            # update status file
            StatusFile.writeFile(
                NextCheckInTime=self.__NextCheckIn,
                LastModifyDates=self.__IMPORTER.getLastModifyDatesFromCache()
            )

            return True

        if (sleeperCheckInFromStatusFile < self.__NextCheckIn):

            logger.debug(
                "Next check in date in file (%s) less than class cached in program (%s)",
                sleeperCheckInFromStatusFile,
                self.__NextCheckIn
            )

            # refresh last and next check in dates
            self.checkIn()

            return True
        # if earlier if statements was not true, return false,
        # as exiting wait loop is not needed
        return False

    def __check_status_file(self, counter: int) -> bool:
        '''
            Method to check if status file should be read, based on configured check interval
        '''
        # +1 <- to skip triggering it for counter == 0,
        # which will occur on the first iteration of main sleep loop
        return (
            (counter + 1) % (self.StatusFileCheckInterval_ms / 1000) == 0
        )

    def __invoke_sleep(self, sleepTime: float):
        '''
            Method to sleep for time remaining to next check in, which allows to receive stop signal
            and actively checks config files changes to update existing config, once file will be updated.
        '''

        logger.debug("__invoke_sleep(%f)", sleepTime)

        # get decimal part of sleep time
        fractionTime = sleepTime % 1

        # get number of full seconds to wait without decimal part
        fullSeconds = int(sleepTime)

        # sleep for fraction time, as it will be less than 1 second
        # and each wait loop iteration will sleep for 1 second
        logger.debug("Sleeping for fraction time: %f", fractionTime)
        time.sleep(fractionTime)

        # Start sleep loop
        logger.debug(
            "Starting main sleep loop. Will be executed: %d times.",
            fullSeconds
        )
        for c in range(0, fullSeconds):

            # check if kill signal was sent, if yes exit the program
            if self.__TERMINATOR.getStatus() == True:
                logger.info("Exiting program with code 0.")
                exit(0)

            # perform check on changes in status and config files
            # on each n -th iteration defined based on StatusFileCheckInterval_ms
            elif self.__check_status_file(c):

                # if returns true - some new data was imported, or next check in time passed
                # exit the wait loop
                if self.__exit_sleep_loop():
                    return None

            # sleep program execution on each for loop iteration
            time.sleep(1)

        # refresh last and next check in dates
        self.checkIn()
        return None

    def checkIn(self) -> None:
        '''
            Method to refresh last and next check in datetimes
        '''
        logger.debug("Refresh last and next check in datetimes")
        self.__last_check_in()
        self.__next_check_in()

        return None

    def getTimeSinceLastCheckIn(self) -> float:
        '''
            Method to calculate time between last check in and now
        '''
        return (
            (
                datetime.now() - self.__LastCheckIn
            )
            .total_seconds()
        )

    def start(self) -> float:
        '''
            Public method to start waiting for next check in time
        '''

        # Get processing time and sleep time
        OperationTime = self.getTimeSinceLastCheckIn()
        logger.info("Operations took: %f", OperationTime)
        TimeToSleep = self.__calculate_time_to_sleep()

        # if sleep time is less than 0 it means that operations took longer,
        # than check interval is set.
        # in this case skip calling sleep and return
        if TimeToSleep <= 0:
            logger.warning(
                "Sleep time exceeded by %f seconds.",
                (TimeToSleep * -1)
            )
        else:

            # invoke sleep until the next check in time
            logger.info("Sleep for: %f seconds", TimeToSleep)
            self.__invoke_sleep(TimeToSleep)

        logger.info("Returning time which process should be sleeping.")
        return TimeToSleep
