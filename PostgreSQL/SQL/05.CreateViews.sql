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
    f.ID AS "fund_id",
    f.F_name AS "fund_name",
    fc.C_name AS "category_name",
    fc.C_shortname AS "category_short",
    f.Currency AS "currency",
    f.F_url AS "fund_url"
FROM Fund f
LEFT JOIN Fund_Category fc ON fc.ID = f.Category_ID;

CREATE VIEW Quotations AS
SELECT
    fq.Quotation_date AS "date",
    fq.fund_id AS "fund_id",
    fq.Quotation_value AS "value",
    fq.Day_value_change AS "daily_change",
    fq.Week_value_change AS "weekly_change",
    fq.Month_value_change AS "monthly_change",
    fq.Year_value_change AS "yearly_change"
FROM Fund_Quotation fq;
