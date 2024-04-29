"""
.DESCRIPTION
    Class to handle signals used in docker containers to stop them.
    

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      28-Apr-2024
    ChangeLog:

    Date            Who                     What
    2024-04-29      Stanisław Horna         Add logging capabilities.

"""
import signal
import logging
from dataclasses import dataclass, field


class Terminator:
    kill_now: bool = field(init=False, default=False)
    signals: dict = {
        signal.SIGINT: 'SIGINT',
        signal.SIGTERM: 'SIGTERM'
    }

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        logging.warning("Stop signal received.")
        self.kill_now = True

    def getStatus(self) -> bool:
        return self.kill_now
