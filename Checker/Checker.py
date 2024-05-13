"""
.DESCRIPTION
    Checker service will check if there are new quotation on the Analizy.pl frontend page.
    Retrieved results will be compared with quotation dates stored in the DB.
    If there is new data available on the Internet, 
    download will be invoked for funds with new quotation found.
    Once funds will be downloaded appropriate investment results will be refreshed.
    

.NOTES

    Version:            1.2
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      25-Apr-2024
    ChangeLog:

    Date            Who                     What
    2024-04-29      Stanisław Horna         Add additional messages for detection that tables are empty.
                                            Add logging capabilities.

"""

from AnalizyPL.Analizy_API import AnalizyAPI
from InvestmentAPI.Investment_API_Handler import InvestmentAPI
from InvestmentAPI.Unpacker import Unpacker
from Utility.Sleeper import Sleeper
from Utility.Exceptions import InvestmentAPIexception, AnalizyAPIexception
from Log.Logger import logger


def Main():

    InvestmentAPI.waitForFullSystemInitialization()

    sleeper = Sleeper()
    try:
        while True:
            try:
                quotationUpdate()
                refundUpdate()
            except InvestmentAPIexception:
                logger.exception(
                    "InvestmentAPI exception occurred", exc_info=True)

            sleeper.start()
    except:
        logger.exception("Exception occurred", exc_info=True)


def quotationUpdate():

    logger.info("quotationUpdate()")

    # Get list of funds to check
    fundsToCheck = (InvestmentAPI.getFunds())

    # If list is empty invoke downloading all fund quotations
    if not fundsToCheck:
        logger.warning("Fund list is empty")
        try:
            logger.debug(str(InvestmentAPI.updateFunds()))

        except InvestmentAPIexception:
            logger.exception(
                "InvestmentAPI exception occurred", exc_info=True)

        except AnalizyAPIexception:
            logger.exception("AnalizyAPI exception occurred", exc_info=True)

        return None

    # Loop through monitored funds
    for item in fundsToCheck:

        try:
            # Unpack response items
            fund_id, fund_cat, quotation_date = (
                Unpacker.fundGetter(item)
            )

            # Download quotation date
            quotation_date_web = AnalizyAPI.getLastQuotationDate(
                fund_id, fund_cat)

            logger.debug(
                "Comparing quotation dates (web | DB): %s, %s",
                quotation_date_web, quotation_date
            )
            # Check if Analizy.pl api has newer quotation available,
            # if yes, then invoke update for particular fund
            if quotation_date_web > quotation_date:
                logger.info(str(InvestmentAPI.updateFunds(fund_id)))

        except InvestmentAPIexception:
            logger.exception(
                "InvestmentAPI exception occurred", exc_info=True)

        except AnalizyAPIexception:
            logger.exception("AnalizyAPI exception occurred", exc_info=True)

    return None


def refundUpdate():

    logger.info("refundUpdate()")

    # Get list of investments to check
    investmentsToCheck = (InvestmentAPI.getInvestment())

    # If list is empty invoke refund calculation for all investments
    if not investmentsToCheck:
        logger.warning("Investment list is empty")
        try:
            logger.debug(str(InvestmentAPI.updateInvestment()))

        except InvestmentAPIexception:
            logger.exception(
                "InvestmentAPI exception occurred", exc_info=True)

        except AnalizyAPIexception:
            logger.exception("AnalizyAPI exception occurred", exc_info=True)

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

            logger.debug(
                "Comparing dates (quotation | refund): %s, %s",
                quotation_date, refund_date
            )
            # Check if quotation date is newer than the calculated refund date,
            # if yes add investment to update set
            if quotation_date > refund_date:
                investmentsToUpdate.add(investment_id)
                logger.debug(
                    "Investment (%s) added to update set", investment_id)

        except InvestmentAPIexception:
            logger.exception(
                "InvestmentAPI exception occurred", exc_info=True)

    # Loop through investments to update
    for investment in investmentsToUpdate:

        try:
            # Trigger investment refund calculation
            logger.info(str(InvestmentAPI.updateInvestment(investment)))

        except InvestmentAPIexception as invErr:
            logger.exception(
                "InvestmentAPI exception occurred", exc_info=True)


if __name__ == '__main__':
    logger.info("Service started")
    Main()
