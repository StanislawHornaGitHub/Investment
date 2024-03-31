/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display last quotation date for each monitored fund


    .NOTES

        Version:            1.0
        Author:             Stanisław Horna
        Mail:               stanislawhorna@outlook.com
        GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
        Creation Date:      30-Mar-2024
        ChangeLog:

        Date            Who                     What

*/

WITH funds_quotation_with_rank AS (
    SELECT
        *,
        ROW_NUMBER () OVER (PARTITION BY fund_id ORDER BY date DESC) AS "rank"
    FROM quotations q
)

SELECT 
    date AS "Date",
    f.fund_id AS "Fund ID",
    fund_name AS "Fund name"
FROM funds_quotation_with_rank fq
LEFT JOIN funds f ON f.FUND_ID = fq.fund_id
WHERE rank = 1