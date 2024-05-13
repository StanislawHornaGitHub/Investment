"""
.DESCRIPTION
    Script file to initialize logger based on the environmental variables.

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      03-May-2024
    ChangeLog:

    Date            Who                     What

"""

import os
import logging
from logging.handlers import RotatingFileHandler
from Log.Logger_formatters import JsonFormatter
from loki_logger_handler.loki_logger_handler import LokiLoggerHandler

LOG_PATH = os.getenv('LOG_PATH', "/log/")
LOG_FILE_NAME = os.getenv('LOG_FILE_NAME', "Checker")

logger = logging.getLogger("Checker")

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(module)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=os.getenv('LOG_LEVEL', "DEBUG")
)

match (os.getenv('LOG_TYPE', "JSON")):

    case "LOKI":

        LOKI_IP = os.getenv("LOKI_IP_Address", "Loki")
        LOKI_PORT = os.getenv("LOKI_PORT", "3100")
        custom_handler = LokiLoggerHandler(
            url=f"http://{LOKI_IP}:{LOKI_PORT}/loki/api/v1/push",
            labels={"Service": "Checker"}
        )
        logger.addHandler(custom_handler)

    case "JSON":
        json_formatter = JsonFormatter(
            {
                "timestamp": "asctime",
                "level": "levelname",
                "module": "module",
                "funcName": "funcName",
                "message": "message",
                "processName": "processName",
                "processID": "process",
                "threadID": "thread"
            }
        )

        file_handler = RotatingFileHandler(
            filename=LOG_PATH+LOG_FILE_NAME+".json",
            mode='w',
            maxBytes=512000,
            backupCount=4
        )

        file_handler.setFormatter(json_formatter)

        logger.addHandler(file_handler)
