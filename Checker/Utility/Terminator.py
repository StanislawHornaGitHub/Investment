"""
.DESCRIPTION
    Class to handle signals used in docker containers to stop them.
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      28-Apr-2024
    ChangeLog:

    Date            Who                     What

"""
import signal
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
        print("\nStop signal received ({} signal)".format(self.signals[signum]))
        self.kill_now = True
        
    def getStatus(self) -> bool:
        return self.kill_now
