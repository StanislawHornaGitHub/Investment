"""
.DESCRIPTION
    Functions to initialize logger based on the environmental variables.
    

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      03-May-2024
    ChangeLog:

    Date            Who                     What
    2024-05-06      Stanisław Horna         add missing I/O datatypes.

"""
import os
import logging
from logging.handlers import RotatingFileHandler
from Utility.Logger_formatters import JsonFormatter
from loki_logger_handler.loki_logger_handler import LokiLoggerHandler
from uwsgidecorators import postfork

DEFAULT_LOG_TYPE = "JSON"


def init_logger_basic() -> logging.Logger:
    logger = logging.getLogger("Flask")

    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d - %(levelname)s - %(module)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=os.getenv('LOG_LEVEL', "DEBUG")
    )
    return logger


@postfork
def init_logger_LOKI() -> logging.Logger:

    # Additional if to avoid creating additional handler post fork
    if os.getenv('LOG_TYPE', DEFAULT_LOG_TYPE) == "LOKI":
        logger = init_logger_basic()
        LOKI_IP = os.getenv("LOKI_IP_Address", "Loki")
        LOKI_PORT = os.getenv("LOKI_PORT", "3100")

        custom_handler = LokiLoggerHandler(
            url=f"http://{LOKI_IP}:{LOKI_PORT}/loki/api/v1/push",
            labels={"Service": "Flask"}
        )
        logger.addHandler(custom_handler)
        return logger


def init_logger_JSON() -> logging.Logger:
    logger = init_logger_basic()
    LOG_PATH = os.getenv('LOG_PATH', "/log/")
    LOG_FILE_NAME = os.getenv('LOG_FILE_NAME', "Flask")
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

    return logger


def init_logging() -> logging.Logger:

    match (os.getenv('LOG_TYPE', DEFAULT_LOG_TYPE)):

        case "LOKI":

            logger = init_logger_LOKI()
        case "JSON":

            logger = init_logger_JSON()

    return logger


logger = init_logging()
