/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display profit over time per investment wallet


    .NOTES

        Version:            1.0
        Author:             Stanisław Horna
        Mail:               stanislawhorna@outlook.com
        GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
        Creation Date:      28-Mar-2024
        ChangeLog:

        Date            Who                     What

*/

SELECT
    result_date AS "time",
    i.investment_name  AS "metric",
    SUM(FUND_VALUE - FUND_INVESTED_MONEY) AS "value"
FROM investment_results ir
INNER JOIN (
    SELECT DISTINCT 
        investment_id, 
        investment_name  
    FROM investments i
    WHERE investment_owner = ${Investment_Owner:singlequote}
) i ON i.investment_id  = ir.investment_id
GROUP BY  RESULT_DATE, i.INVESTMENT_NAME;