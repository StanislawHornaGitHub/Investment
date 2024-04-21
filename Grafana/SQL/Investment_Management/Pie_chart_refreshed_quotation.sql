/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display pie chart of refreshed fund's quotation


    .NOTES

        Version:            1.1
        Author:             Stanisław Horna
        Mail:               stanislawhorna@outlook.com
        GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
        Creation Date:      04-Apr-2024
        ChangeLog:

        Date            Who                     What
        2024-04-21      Stanisław Horna         Table usage replaced with views.

*/

WITH refreshed_funds AS (
    SELECT 
        COUNT(*) AS "Refreshed"
    FROM quotations
    WHERE date = (
        SELECT 
            MAX(date)
        FROM quotations 
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
