/*
    .DESCRIPTION
        SQL script for PostgreSQL to configure Views in Investments DB.
        EXISTING DB VIEWS WILL BE REMOVED AND PRIVILEGES WILL BE FLUSHED.

		Following actions will be performed in a given order:
			1. DROP of all TravelNest Views.
			2. CREATE all Views from scratch.


	.RULES
		- DROP VIEW must include IF EXISTS.

		- Required columns must be defined with table alias for better visibility.

		- Aliases for VIEW columns must contain view name, column name in format:
			<view_name>_<column_name>


    .NOTES

        Version:            1.0
        Author:             Stanisław Horna
        Mail:               stanislawhorna@outlook.com
        GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
        Creation Date:      24-Mar-2024
        ChangeLog:

        Date            Who                     What

*/

CREATE VIEW Funds AS
SELECT
    f.ID,
    f.F_name,
    fc.C_name,
    f.Currency,
    f.F_url
FROM Fund f
LEFT JOIN Fund_Category fc ON fc.ID = f.Category_ID;
