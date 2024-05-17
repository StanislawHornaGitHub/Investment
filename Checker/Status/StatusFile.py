"""
.DESCRIPTION
    Class to handle status file operations


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
import yaml
import datetime
from Log.Logger import logger


class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


class StatusFile:
    __file_path: str = os.getenv(
        'STATUS_FILE_PATH', '/var/lib/checker/status.yaml'
    )

    NEXT_CHECK_IN_LABEL: str = "NextCheckIn"
    LAST_MODIFY_DATES_LABEL: str = "LastModified"

    @staticmethod
    def readFile() -> dict[str, datetime.datetime | list[datetime.datetime]]:
        '''
            Method to read YAML status file if exists.
            returns file content in dict if read was successful,
            otherwise empty dict is returned
        '''

        # check if status file exists
        if os.path.exists(StatusFile.__file_path):
            logger.debug("Status file found")

            # try to read status file and parse it to dict,
            # if operation was successful return read data
            try:
                with open(StatusFile.__file_path, 'r') as yaml_file:
                    data = yaml.safe_load(yaml_file)
                    logger.debug("Status file loaded successfully")
                    return data
            except:
                logger.exception("Failed to load status file", exc_info=True)
                return {}
        else:
            logger.debug("Status file NOT found")
            return {}

    @staticmethod
    def writeFile(NextCheckInTime: datetime, LastModifyDates: dict[str, datetime.datetime]) -> bool:
        '''
            Method to write status info to file.
            Returns True if it was successful, otherwise returns False
        '''

        # get valid dict structure to write it to yaml file
        logger.debug("Creating output dict structure for status file")
        dataToSave = StatusFile.__get_data_to_yaml_file(
            NextCheckInTime, LastModifyDates)

        # try to write status file,
        # if operation was successful return True
        try:
            with open(StatusFile.__file_path, 'w') as file:
                yaml.dump(
                    dataToSave,
                    file,
                    Dumper=IndentDumper
                )
            logger.debug("Status file successfully saved on hard drive")

            return True
        except:
            logger.exception("Failed to saver status file", exc_info=True)

            return False

    @staticmethod
    def __get_data_to_yaml_file(NextCheckInTime: datetime, LastModifyDates: dict[str, datetime.datetime]) -> dict:
        '''
            Method to create desired dict for valid YAML file
        '''
        dataToSave = {}
        dataToSave[StatusFile.NEXT_CHECK_IN_LABEL] = NextCheckInTime
        dataToSave[StatusFile.LAST_MODIFY_DATES_LABEL] = LastModifyDates

        logger.debug("Output dict for status file created successfully")
        return dataToSave
