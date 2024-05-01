import os
import logging
from loki_logger_handler.loki_logger_handler import LokiLoggerHandler


logger = logging.getLogger("Checker")
LOKI_IP = os.getenv("LOKI_IP_Address", "Loki")
LOKI_PORT = os.getenv("LOKI_PORT", "3100")
custom_handler = LokiLoggerHandler(
    url=f"http://{LOKI_IP}:{LOKI_PORT}/loki/api/v1/push",
    labels={"Service": "Checker"}
)
logger.addHandler(custom_handler)

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(module)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=os.getenv('LOG_LEVEL', "DEBUG")
)
