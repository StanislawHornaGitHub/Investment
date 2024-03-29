/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display refund per week by investment wallet


    .NOTES

        Version:            1.0
        Author:             Stanisław Horna
        Mail:               stanislawhorna@outlook.com
        GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
        Creation Date:      29-Mar-2024
        ChangeLog:

        Date            Who                     What

*/

SELECT
    result_date AS "time",
    i.investment_name  AS "metric",
    SUM(last_week_result/ fund_invested_money) * 100 AS "value"
FROM investment_results ir
INNER JOIN (
    SELECT DISTINCT 
        investment_id, 
        investment_name  
    FROM investments i
    WHERE investment_owner = ${Investment_Owner:singlequote}
) i ON i.investment_id  = ir.investment_id
GROUP BY result_date, i.investment_name;