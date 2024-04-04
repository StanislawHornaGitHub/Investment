/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display profit over time per investment wallet


    .NOTES

        Version:            1.1
        Author:             Stanisław Horna
        Mail:               stanislawhorna@outlook.com
        GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
        Creation Date:      28-Mar-2024
        ChangeLog:

        Date            Who                     What
        2024-04-04      Stanisław Horna         Additional condition in WHERE clause of outer query added,
                                                to avoid displaying graph without having investment results,
                                                for all funds collected under particular investment.
                                                
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
WHERE 
    FUND_INVESTED_MONEY <> 0 AND
        ( -- Get number of funds in investment with ID from outer query
            SELECT 
                COUNT(*)
            FROM (
                SELECT DISTINCT 
                    investment_fund_id 
                FROM investments
                WHERE 
                    investment_id = i.investment_id 
            )
        ) = ( -- Get number of results for current day in investment with ID from outer query
            SELECT
                COUNT(*)
            FROM (
                SELECT
                    fund_id
                FROM investment_results
                WHERE 
                    investment_id = i.investment_id AND
                    result_date = ir.result_date
            )
        )
GROUP BY  RESULT_DATE, i.INVESTMENT_NAME;