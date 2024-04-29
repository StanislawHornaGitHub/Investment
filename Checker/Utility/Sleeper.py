"""
.DESCRIPTION
    Class to handle sleeping the process between operations.
    

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      28-Apr-2024
    ChangeLog:

    Date            Who                     What
    2024-04-29      Stanisław Horna         add check-in after completed sleep.

"""
import time
import sys
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

        fractionTime = sleepTime % 1
        fullSeconds = int(sleepTime)

        time.sleep(fractionTime)

        for c in range(0, fullSeconds):
            if self.__TERMINATOR.getStatus() == True:
                exit(0)

            time.sleep(1)
        
        self.checkIn()

    def checkIn(self) -> None:
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

        OperationTime = self.getTimeSinceLastCheckIn()
        TimeToSleep = self.__calculate_time_to_sleep()

        if TimeToSleep <= 0:
            print(
                "Operations took: ",
                OperationTime, " seconds. ",
                "Sleep time exceeded by ",
                (TimeToSleep * -1), " seconds."
            )
        else:
            print(
                "Operations took: ",
                OperationTime, " seconds. ",
                "Sleep for: ",
                TimeToSleep, " seconds"
            )
            self.__invoke_sleep(TimeToSleep)

        return TimeToSleep
