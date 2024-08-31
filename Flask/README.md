# Main API
The main application API, which is responsible for retrieving data and calculating the results stored in [Database](/PostgreSQL/README.md).

It directly connects to [PostgreSQL DB](/PostgreSQL/README.md) using SQL Alchemy, to perform CRUD operations on Database.

Runs under uwsgi server inside of Docker container.

# Processing Classes

## Fund Config class
The **FundConfig** class provides a set of static methods for managing fund configurations,
importing fund data from JSON files, and retrieving fund information from a database. 
It is designed to handle fund insertion, manage error cases like duplicate entries, 
and fetch the latest fund quotations. 
The class uses SQLAlchemy sessions for database transactions 
and includes robust logging for debugging and error handling.

## Investment Calc Result class
The **InvestmentCalcResult** class is a core component designed to calculate and manage investment performance results 
over various time periods, such as daily, weekly, monthly, and yearly. 
This class provides functionalities to calculate the results for all investments or a specific investment, 
ensuring accurate and up-to-date financial data. 
It interacts with a database to fetch necessary data and store the results.

## Investment Config class
The **InvestmentConfig** class is a comprehensive utility for managing investment data in Python. 
It provides various static methods to insert, retrieve, and manage investment records, 
ensuring proper handling of transactions, error management, and database interactions. 

## Price class
The **Price** class is designed to handle the updating and insertion of fund quotations in application database.
It provides static methods to manage the retrieval of the latest fund prices, the insertion of new price records into the database, and the calculation of returns over different time periods.