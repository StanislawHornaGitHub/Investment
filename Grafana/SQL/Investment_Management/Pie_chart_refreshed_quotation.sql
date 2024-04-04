/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display pie chart of refreshed fund's quotation


    .NOTES

        Version:            1.0
        Author:             Stanisław Horna
        Mail:               stanislawhorna@outlook.com
        GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
        Creation Date:      04-Apr-2024
        ChangeLog:

        Date            Who                     What

*/

WITH refreshed_funds AS (
    SELECT 
        COUNT(*) AS "Refreshed"
    FROM fund_quotation
    WHERE quotation_date = (
        SELECT 
            MAX(quotation_date)
        FROM fund_quotation 
    )
),

all_funds AS (
    SELECT
        COUNT(*) AS "All funds"
    FROM funds
)

SELECT
    "Refreshed",
    ("All funds" - "Refreshed") AS "Not refreshed"
FROM refreshed_funds, all_funds
