"""
.DESCRIPTION
    Class to handle importing data to system form JSON config files.
    Supports inserting Funds to monitor and investments.
    Allows to add to existing investments new entries.

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      14-May-2024
    ChangeLog:

    Date            Who                     What
    2024-05-17      Stanisław Horna         Documented code. Enabled logging.

"""

import os
import json
import fnmatch
import datetime
from dataclasses import dataclass, field
from InvestmentAPI.Investment_API_Handler import InvestmentAPI
from Status.StatusFile import StatusFile
from Utility.Exceptions import InvestmentAPIexception
from Log.Logger import logger


@dataclass
class DataImporter:

    __config_directory: str = field(
        init=False,
        default=os.getenv('CONFIG_ROOT_PATH', '/etc/checker')
    )
    __fund_config_dir: str = field(
        init=False,
        default=os.getenv('CONFIG_FUND_DIR', 'fund')
    )
    __investment_config_dir: str = field(
        init=False,
        default=os.getenv('CONFIG_INVESTMENT_DIR', 'investment')
    )

    __old_date: datetime.datetime = field(
        init=False,
        default=datetime.datetime(1900, 1, 1)
    )

    files_last_modify_dates: dict[str, float] = field(
        init=False,
        default_factory=dict
    )

    def putChangedConfigs(self, statusFileContent: dict[str, datetime.datetime] = {}) -> bool:
        '''
            Method to insert updated configs to system if something was changed.
            Compares last modify dates of actual files, with those received as variable,
            based on the output invokes importing funds and investments.

            Returns True if anything was imported.
        '''

        # assign last modify dates to class attribute
        logger.debug("Params: %s", statusFileContent)
        self.files_last_modify_dates = statusFileContent

        importStatus = []

        logger.debug("Importing funds")
        importStatus.append(
            self.importFunds()
        )
        logger.debug("Importing investments")
        importStatus.append(
            self.importInvestments()
        )

        if True in importStatus:
            logger.debug("Some config was imported to the system")
            return True
        else:
            logger.warning("No config was imported")
            return False

    def getLastModifyDatesFromStatusFile(self) -> None:
        '''
            Method to extract dict with last modify dates of config files
        '''
        statusFile = StatusFile.readFile()
        self.files_last_modify_dates = (
            statusFile
            .get(StatusFile.LAST_MODIFY_DATES_LABEL, {})
        )
        return None

    def getLastModifyDatesFromCache(self) -> dict[str, datetime.datetime]:
        return self.files_last_modify_dates

    def importFunds(self) -> bool:
        '''
            Method to import funds configs to the system.
        '''

        output: list[bool] = []
        # get last modify dates from file system
        logger.debug(
            "Listing files in fund configuration directory (%s)",
            DataImporter.__fund_config_dir
        )
        try:
            modifyDates = (
                DataImporter
                .__get_files_to_last_modify_date(
                    DataImporter.__fund_config_dir
                )
            )
        except:
            logger.exception(
                "Failed to list files",
                exc_info=True
            )

        # loop through each file in fund config directory
        for file in modifyDates:

            # check if date from status file is older than actual date in file system
            if (StatusFileDate := self.files_last_modify_dates.get(file, DataImporter.__old_date)) < modifyDates[file]:

                logger.debug(
                    "Last modify date from file (%s) is less than the date read out from file system (%s)",
                    StatusFileDate,
                    modifyDates[file]
                )

                # try to read config file
                logger.debug("Reading %s fund config file", file)
                try:
                    data = DataImporter.__import_config_from_file(
                        DataImporter.__fund_config_dir,
                        file
                    )
                except:
                    logger.exception("Failed to read %s", file, exc_info=True)
                    output.append(False)
                    continue

                # try to import content of config file to system
                logger.debug("Importing %s fund config file to system", file)
                try:
                    InvestmentAPI.putFunds(data)
                    output.append(True)
                    self.files_last_modify_dates[file] = modifyDates[file]
                except:
                    logger.exception(
                        "Failed to import data to system",
                        exc_info=True
                    )
                    output.append(False)
            else:
                # to handle cases where file was reverted to previous version with metadata
                self.files_last_modify_dates[file] = modifyDates[file]

        if True in output:
            logger.warning("Fund configs imported")
            return True
        else:
            logger.debug("No funds imported")
            return False

    def importInvestments(self) -> bool:
        '''
            Method to import investment configs to the system.
        '''

        output: list[bool] = []
        # get last modify dates from file system
        logger.debug(
            "Listing files in investment configuration directory (%s)",
            DataImporter.__investment_config_dir
        )
        try:
            modifyDates = (
                DataImporter
                .__get_files_to_last_modify_date(
                    DataImporter.__investment_config_dir
                )
            )
        except:
            logger.exception(
                "Failed to list files",
                exc_info=True
            )

        # loop through each file in fund config directory
        for file in modifyDates:

            if (StatusFileDate := self.files_last_modify_dates.get(file, DataImporter.__old_date)) < modifyDates[file]:

                logger.debug(
                    "Last modify date from file (%s) is less than the date read out from file system (%s)",
                    StatusFileDate,
                    modifyDates[file]
                )
                # try to read config file
                logger.debug("Reading %s investment config file", file)
                try:
                    data = DataImporter.__import_config_from_file(
                        DataImporter.__investment_config_dir,
                        file
                    )
                except:
                    logger.exception("Failed to read %s", file, exc_info=True)
                    output.append(False)
                    continue

                # try to import content of config file to system
                logger.debug(
                    "Importing %s investment config file to system",
                    file
                )
                try:
                    InvestmentAPI.putInvestments(data)
                    output.append(True)
                    self.files_last_modify_dates[file] = modifyDates[file]
                except:
                    logger.exception(
                        "Failed to import data to system",
                        exc_info=True
                    )
                    output.append(False)
            else:
                # to handle cases where file was reverted to previous version with metadata
                self.files_last_modify_dates[file] = modifyDates[file]

        if True in output:
            logger.warning("Investment configs imported")
            return True
        else:
            logger.debug("No investments imported")
            return False

    @staticmethod
    def __get_files_to_last_modify_date(directory: str) -> dict[str, datetime.datetime]:
        '''
            Method to get last modify dates from file system
        '''
        output:  dict[str, datetime.datetime] = {}

        # create absolute path to look for files
        pathToLookUp = os.path.join(
            DataImporter.__config_directory,
            directory
        )

        logger.debug("Listing .json files in path: %s", pathToLookUp)
        try:
            filesList = [
                f for f in os.listdir(pathToLookUp)
                if fnmatch.fnmatch(f, '*.json')
            ]
        except:
            logger.exception(
                "Failed to get list of .json config files",
                exc_info=True
            )

        for fileName in filesList:
            filePath = os.path.join(
                pathToLookUp,
                fileName
            )
            try:
                lastModifiedDate = os.path.getmtime(filePath)
                output[fileName] = (
                    datetime.datetime
                    .fromtimestamp(lastModifiedDate)
                )
            except:
                logger.exception(
                    "Failed to get last modify date of %s",
                    fileName,
                    exc_info=True
                )

        return output

    @staticmethod
    def __import_config_from_file(directory: str, fileName: str) -> dict:
        filePath = os.path.join(
            DataImporter.__config_directory,
            directory,
            fileName
        )
        logger.debug("Reading file %s", filePath)
        try:
            with open(filePath, 'r') as file:
                data: dict | list = json.loads(
                    "".join(
                        file.readlines()
                    )
                )
        except:
            logger.exception("Failed to read %s", fileName, exc_info=True)
        return data
