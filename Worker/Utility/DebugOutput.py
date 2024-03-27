import csv
import json

class CSV_writer:
    
    
    @staticmethod
    def saveFile(outputToSave, destinationPath: str = 'test.csv'):
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
    def saveFile(outputToSave, destinationPath: str = 'test.json'):
        try:
            with open(destinationPath, "w") as destinationFileJSON:
                destinationFileJSON.write(json.dumps(outputToSave, indent=4))
        except:
            print("Failed to save the object")
            
        return None