# Main API
The main application API, which is responsible for retrieving data and calculating the results stored in [Database](/PostgreSQL/README.md).

It directly connects to [PostgreSQL DB](/PostgreSQL/README.md) using SQL Alchemy, to perform CRUD operations on Database.

Runs under uwsgi server inside of Docker container.