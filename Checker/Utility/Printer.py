"""
.DESCRIPTION
    Class to help in printing complex structures in console
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      28-Apr-2024
    ChangeLog:

    Date            Who                     What

"""
import json


class Printer:
    
    __json_structure_indent: int = 2

    @staticmethod
    def json(object: any) -> None:
        print (
            json.dumps(
                obj=object,
                indent=Printer.__json_structure_indent
            )
        )
