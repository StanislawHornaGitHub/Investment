"""
.DESCRIPTION
    Checker service will check if there are new quotation on the Analizy.pl frontend page.
    Retrieved results will be compared with quotation dates stored in the DB.
    If there is new data available on the Internet, 
    download will be invoked for funds with new quotation found.
    Once funds will be downloaded appropriate investment results will be refreshed.
    

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      25-Apr-2024
    ChangeLog:

    Date            Who                     What
    2024-04-29      Stanisław Horna         Add additional messages for detection that tables are empty.

"""
from InvestmentAPI.Investment_API_Handler import InvestmentAPI
from InvestmentAPI.Unpacker import Unpacker
from AnalizyPL.API import AnalizyAPI
from Utility.Sleeper import Sleeper
from Utility.Exceptions import InvestmentAPIexception, AnalizyAPIexception
from Utility.Printer import Printer

def Main():

    InvestmentAPI.waitForFullSystemInitialization()
    
    sleeper = Sleeper()

    while True:
        try:
            quotationUpdate()
            refundUpdate()
        except InvestmentAPIexception as invErr:
            print(invErr)

        sleeper.start()


def quotationUpdate():

    # Get list of funds to check
    fundsToCheck = (InvestmentAPI.getFunds())
    
    # If list is empty invoke downloading all fund quotations
    if not fundsToCheck:
        print("Fund list is empty")
        try:
            Printer.json(InvestmentAPI.updateFunds())
            
        except InvestmentAPIexception as invErr:
            print(invErr)

        except AnalizyAPIexception as anaErr:
            print(anaErr)
    
        return None
    
    # Loop through monitored funds
    for item in fundsToCheck:

        try:
            # Unpack response items
            fund_id, fund_cat, quotation_date = (
                Unpacker.fundGetter(item)
            )

            # Check if Analizy.pl api has newer quotation available,
            # if yes, then invoke update for particular fund
            if AnalizyAPI.getLastQuotationDate(fund_id, fund_cat) > quotation_date:
                Printer.json(InvestmentAPI.updateFunds(fund_id))

        except InvestmentAPIexception as invErr:
            print(invErr)

        except AnalizyAPIexception as anaErr:
            print(anaErr)
    
    return None


def refundUpdate():
    
    # Get list of investments to check
    investmentsToCheck = (InvestmentAPI.getInvestment())
    
    # If list is empty invoke refund calculation for all investments
    if not investmentsToCheck:
        print("Investment list is empty")
        try:
            Printer.json(InvestmentAPI.updateInvestment())
            
        except InvestmentAPIexception as invErr:
            print(invErr)

        except AnalizyAPIexception as anaErr:
            print(anaErr)
    
        return None
    

    # Init local set of investment IDs to trigger update
    investmentsToUpdate = set()

    # Loop through configured investments
    for item in investmentsToCheck:

        try:
            # Unpack response items
            investment_id, fund_id, refund_date = (
                Unpacker.investmentGetter(item)
            )

            # Get quotation date for current fund
            _, _, quotation_date = (
                Unpacker.fundGetter(
                    InvestmentAPI.getFunds(fund_id)
                )
            )

            # Check if quotation date is newer than the calculated refund date,
            # if yes add investment to update set
            if quotation_date > refund_date:
                investmentsToUpdate.add(investment_id)

        except InvestmentAPIexception as invErr:
            print(invErr)

    # Loop through investments to update
    for investment in investmentsToUpdate:

        try:
            # Trigger investment refund calculation
            Printer.json(InvestmentAPI.updateInvestment(investment))

        except InvestmentAPIexception as invErr:
            print(invErr)


if __name__ == '__main__':
    Main()
