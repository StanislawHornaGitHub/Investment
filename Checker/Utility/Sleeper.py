"""
.DESCRIPTION
    Class to handle sleeping the process between operations.


.NOTES

    Version:            1.2
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      28-Apr-2024
    ChangeLog:

    Date            Who                     What
    2024-04-29      Stanisław Horna         Add check-in after completed sleep.
                                            Add logging capabilities.


"""
import time
import sys
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from Utility.Terminator import Terminator


@dataclass
class Sleeper:

    TimeInterval_ms: int = field(init=True, default=3600000)

    __TERMINATOR: Terminator = field(init=False, default=Terminator())

    __LastCheckIn: datetime = field(init=False)
    __NextCheckIn: datetime = field(init=False)

    def __post_init__(self):
        self.checkIn()
        logging.debug(
            "Sleeper initialized for interval: %d",
            self.TimeInterval_ms
        )

    def __last_check_in(self):
        self.__LastCheckIn = datetime.now()

    def __next_check_in(self):
        self.__NextCheckIn = (
            self.__LastCheckIn + timedelta(
                milliseconds=self.TimeInterval_ms
            )
        )

    def __calculate_time_to_sleep(self) -> float:

        TimeToSleep = (
            (
                self.__NextCheckIn - datetime.now()
            )
            .total_seconds()
        )
        self.checkIn()
        return TimeToSleep

    def __invoke_sleep(self, sleepTime: float):

        logging.debug("__invoke_sleep(%f)", sleepTime)

        fractionTime = sleepTime % 1
        fullSeconds = int(sleepTime)

        logging.debug("Sleeping for fraction time: %f", fractionTime)
        time.sleep(fractionTime)

        logging.debug(
            "Starting main sleep loop. Will be executed: %d times.", fullSeconds)
        for c in range(0, fullSeconds):
            if self.__TERMINATOR.getStatus() == True:
                logging.info("Exiting program with code 0.")
                exit(0)

            time.sleep(1)

        self.checkIn()

    def checkIn(self) -> None:
        logging.debug("checkIn()")
        self.__last_check_in()
        self.__next_check_in()

        return None

    def getTimeSinceLastCheckIn(self) -> float:
        return (
            (
                datetime.now() - self.__LastCheckIn
            )
            .total_seconds()
        )

    def start(self) -> float:

        logging.debug("start()")

        OperationTime = self.getTimeSinceLastCheckIn()
        logging.info("Operations took: %f", OperationTime)
        TimeToSleep = self.__calculate_time_to_sleep()

        if TimeToSleep <= 0:
            logging.warning(
                "Sleep time exceeded by %f seconds.",
                (TimeToSleep * -1)
            )
        else:
            logging.info("Sleep for: %f seconds", TimeToSleep)

            self.__invoke_sleep(TimeToSleep)

        logging.info("Returning time which process was sleeping.")
        return TimeToSleep
