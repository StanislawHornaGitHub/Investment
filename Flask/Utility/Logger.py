import os
import logging
from loki_logger_handler.loki_logger_handler import LokiLoggerHandler
from uwsgidecorators import postfork


@postfork
def init_logging():
    LOKI_IP = os.getenv("LOKI_IP_Address", "Loki")
    LOKI_PORT = os.getenv("LOKI_PORT", "3100")
    logger = logging.getLogger("Flask")
    custom_handler = LokiLoggerHandler(
        url=f"http://{LOKI_IP}:{LOKI_PORT}/loki/api/v1/push",
        labels={"Service": "Flask"}
    )
    logger.addHandler(custom_handler)

    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d - %(levelname)s - %(module)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=os.getenv('LOG_LEVEL', "DEBUG")
    )
    return logger


logger = init_logging()
