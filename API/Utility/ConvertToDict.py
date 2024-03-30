from SQL.Fund import Fund

class ConvertToDict:
    
    @staticmethod
    def fundList(fund: dict[str, Fund]):
        result = {}
        for f in fund:
            result[f.getFundID()] = f
            
        return result