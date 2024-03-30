/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display last oldest result date for each investment.


    .NOTES

        Version:            1.0
        Author:             Stanisław Horna
        Mail:               stanislawhorna@outlook.com
        GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
        Creation Date:      30-Mar-2024
        ChangeLog:

        Date            Who                     What

*/

WITH investment_results_with_rank AS (
    SELECT
        *,
        ROW_NUMBER () OVER (PARTITION BY fund_id, investment_id ORDER BY result_date DESC) AS "rank"
    FROM investment_results ir
)

SELECT 
    result_date AS "Date",
    investment_name AS "Investment name",
    investment_owner AS "Owner"
FROM (
        SELECT 
            investment_id,
            MIN(result_date) as "result_date"
        FROM investment_results_with_rank
        WHERE rank = 1
        GROUP BY investment_id
) AS r
LEFT JOIN (
        SELECT DISTINCT 
            investment_id, 
            investment_name,
            investment_owner
        FROM investments i
) AS i ON i.investment_id = r.investment_id

