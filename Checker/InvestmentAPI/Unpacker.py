"""
.DESCRIPTION
    Class to easier read Flask api response
    

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      28-Apr-2024
    ChangeLog:

    Date            Who                     What

"""
import datetime

class Unpacker:
    
    @staticmethod
    def fundGetter(entry: list[dict] | dict) -> tuple[str, str, datetime.date]:
        if type(entry) == list:
            return entry[0]["fund_id"], entry[0]["fund_category"], entry[0]["quotation_date"]
        else:
            return entry["fund_id"], entry["fund_category"], entry["quotation_date"]
    
    @staticmethod
    def investmentGetter(entry: list[dict] | dict) -> tuple[int, str, datetime.date]:
        if type(entry) == list:
            return entry[0]["investment_id"], entry[0]["fund_id"], entry[0]["refund_date"]
        else:
            return entry["investment_id"], entry["fund_id"], entry["refund_date"]
    
    @staticmethod
    def fundPutter(entry: list[dict]) -> tuple[str, str, datetime.date]:
        return entry["fund_id"], entry["Status"]