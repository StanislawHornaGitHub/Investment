"""
.DESCRIPTION
    Utility class definition for exporting data to files, which can help in debugging,
    especially calculation related subjects.
    

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
    Creation Date:      27-Mar-2024
    ChangeLog:

    Date            Who                     What
    2024-05-06      Stanisław Horna         add missing I/O datatypes.

"""

import csv
import json


class CSV_writer:

    @staticmethod
    def saveFile(outputToSave: list[dict[str, str]], destinationPath: str = 'test.csv') -> None:
        try:
            with open(destinationPath, "w") as investHistory:
                # Init CSV writer and write headers to the file
                writer = csv.writer(investHistory, delimiter='\t')

                # write headers to file
                writer.writerow(list(outputToSave[0].keys()))

                # loop through each calculated date
                for i in range(0, len(outputToSave)):

                    # convert values for current date to list and write them to file
                    writer.writerow(
                        list(
                            outputToSave[i].values()
                        )
                    )
        except:
            print("Failed to save the object")
        return None


class JSON_writer:

    @staticmethod
    def saveFile(outputToSave: list[dict[str, str]], destinationPath: str = 'test.json') -> None:
        try:
            with open(destinationPath, "w") as destinationFileJSON:
                destinationFileJSON.write(json.dumps(outputToSave, indent=4))
        except:
            print("Failed to save the object")

        return None
