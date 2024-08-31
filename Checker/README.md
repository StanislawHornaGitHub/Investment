# Checker service
Service responsible for importing data to the system and periodically check if there are new quotation available to download.

## Data import
It will automatically scan `./Configs` directory and import them to the system. 
Mentioned directory is periodically checked (by default every 60s),
whether any config file changed. 
If any file was updated it will automatically import that data to the system.

## Quotation Checker
Periodically checks (by default every 1h) 
if there are new fund quotation available by fetching latest data 
and comparing it with the information already stored in database.
If fresh quotation is detected it calls the main application API to fetch new quotation and recalculate positions, which depends on it.