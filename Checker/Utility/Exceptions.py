"""
.DESCRIPTION
    Custom exception classes definition.
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      28-Apr-2024
    ChangeLog:

    Date            Who                     What

"""
class InvestmentAPIexception(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
        
class AnalizyAPIexception(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)