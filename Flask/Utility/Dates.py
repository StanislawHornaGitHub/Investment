"""
.DESCRIPTION
    Utility class definition for date related operation
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      27-Mar-2024
    ChangeLog:

    Date            Who                     What

"""

from dateutil.parser import parse
import datetime

class Dates:
    
    Daily = 1
    Weekly = 7
    Monthly = 30
    Yearly = 365
    
    @staticmethod
    def getDesiredDates(currentDate: datetime) -> dict[str, datetime.datetime]:
        return {
            'daily': (currentDate - datetime.timedelta(
                days=Dates.Daily
            )),
            'weekly': (currentDate - datetime.timedelta(
                days=Dates.Weekly
            )),
            'monthly': (currentDate - datetime.timedelta(
                days=Dates.Monthly
            )),
            'yearly': (currentDate - datetime.timedelta(
                days=Dates.Yearly
            )),
        }
    
    @staticmethod
    def getEntryWithDesiredDate(inputData, dateFieldName, desiredDate):
        i = len(inputData)
        while (i:= i -1) >= 0:
            if inputData[i][dateFieldName] <= desiredDate:
                return inputData[i]
        
        return None
        
    @staticmethod
    def addDays(date: datetime.datetime, days: int) -> datetime.datetime:
        return (
            date + datetime.timedelta(days=days)
            )
        
    @staticmethod
    def convertDateToString(date: datetime.datetime, outFormat: str =  "%Y-%m-%d") -> str:
        return date.strftime(outFormat)