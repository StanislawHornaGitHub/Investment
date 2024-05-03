"""
.DESCRIPTION
    Class with custom log formatter to create log files, where each line is a JSON structure.
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      03-May-2024
    ChangeLog:

    Date            Who                     What

"""
import logging
import json
from datetime import datetime


class JsonFormatter(logging.Formatter):

    def __init__(self, fmt_dict: dict = None, time_format: str = "%Y-%m-%d %H:%M:%S.%f"):
        self.fmt_dict = fmt_dict if fmt_dict is not None else {
            "message": "message"
        }
        self.default_time_format = "%Y-%m-%d %H:%M:%S"
        self.datefmt = time_format

    def formatTime(self, record, datefmt=None):

        # read out time from record object
        created_time = record.created

        # convert time to datetime
        dt_object = datetime.fromtimestamp(created_time)

        # format with provided pattern
        return dt_object.strftime(datefmt)

    def usesTime(self) -> bool:

        return "asctime" in self.fmt_dict.values()

    def formatMessage(self, record) -> dict:

        return {fmt_key: record.__dict__[fmt_val] for fmt_key, fmt_val in self.fmt_dict.items()}

    def format(self, record) -> str:

        # read out message from record
        record.message = record.getMessage()

        # format time it it is in use
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        # create dictionary message
        message_dict = self.formatMessage(record)

        # add additional properties related to exception and stack data
        if record.exc_info:

            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message_dict["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        # return formatted json structure
        return json.dumps(message_dict, default=str)
