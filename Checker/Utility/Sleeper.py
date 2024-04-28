"""
.DESCRIPTION
    Class to handle sleeping the process between operations.
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      28-Apr-2024
    ChangeLog:

    Date            Who                     What

"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
import time


@dataclass
class Sleeper:

    TimeInterval_ms: int = field(init=True, default=10000)

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
    
    def checkIn(self) -> None:
        self.__last_check_in()
        self.__next_check_in()
        
        return None

    def start(self) -> float:

        TimeToSleep = self.__calculate_time_to_sleep()

        if TimeToSleep <= 0:
            print("Sleep time exceeded by ", (TimeToSleep * -1), " seconds")
        else:
            print("Sleep for: ", TimeToSleep, " seconds")
            time.sleep(TimeToSleep)

        return TimeToSleep
