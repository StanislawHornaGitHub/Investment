"""
.DESCRIPTION
    Class to help in printing complex structures in console
    

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      28-Apr-2024
    ChangeLog:

    Date            Who                     What
    2024-04-29      Stanisław Horna         Add try-except block,
                                            to avoid exiting process in case of errors with displaying messages.
"""
import json


class Printer:

    __json_structure_indent: int = 2

    @staticmethod
    def json(object: any) -> None:
        try:
            print(
                json.dumps(
                    obj=object,
                    indent=Printer.__json_structure_indent,
                    default=str
                )
            )
        except:
            print(object)
