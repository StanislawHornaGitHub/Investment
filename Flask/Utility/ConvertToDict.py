"""
.DESCRIPTION
    Utility class definition to convert particular objects to dictionaries.
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      27-Mar-2024
    ChangeLog:

    Date            Who                     What

"""

from SQL.Fund import Fund

class ConvertToDict:
    
    @staticmethod
    def fundList(fund: list[Fund]):
        result = {}
        for f in fund:
            result[f.getFundID()] = f
            
        return result