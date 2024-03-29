/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display sum of overall profit of all investments


    .NOTES

        Version:            1.0
        Author:             Stanisław Horna
        Mail:               stanislawhorna@outlook.com
        GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
        Creation Date:      28-Mar-2024
        ChangeLog:

        Date            Who                     What
        2024-03-29      Stanisław Horna         Changed to CTE to have the proper result,
                                                if not all funds have new quotations
*/

WITH results_with_rank AS (
    SELECT
        *,
        ROW_NUMBER () OVER (PARTITION BY fund_id, investment_id ORDER BY result_date DESC) as "rank"
    FROM investment_results

),

filtered_investment_results AS (
	SELECT 
		*
	from results_with_rank
	WHERE  rank = 1
),

refund_per_investment AS (
    SELECT
        SUM(FUND_VALUE - FUND_INVESTED_MONEY) AS "Profit"
    FROM filtered_investment_results ir
    INNER JOIN (
        SELECT DISTINCT 
            investment_id, 
            investment_name  
        FROM investments i
        WHERE investment_owner = ${Investment_Owner:singlequote}
    ) i ON i.investment_id  = ir.investment_id
)
SELECT 
    * 
FROM refund_per_investment