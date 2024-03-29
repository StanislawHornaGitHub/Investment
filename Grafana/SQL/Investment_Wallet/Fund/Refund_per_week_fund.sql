/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display fund percentage refund per week.


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
    result_date AS time,
    fund_name AS metric,
    (last_week_result / fund_invested_money) * 100 AS value
FROM investment_results ir 
LEFT JOIN funds f ON f.fund_id = ir.fund_id
WHERE investment_id IN (
    SELECT DISTINCT
        investment_id
    FROM investments
    WHERE investment_owner = ${Investment_Owner:singlequote}
);