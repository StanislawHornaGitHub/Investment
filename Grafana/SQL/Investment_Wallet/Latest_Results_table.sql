/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display investment results like in table similar to the first console one


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
        ROW_NUMBER () OVER (PARTITION BY fund_id, investment_id ORDER BY result_date DESC) AS "rank"
    FROM investment_results
    WHERE investment_id IN (
        SELECT DISTINCT
            investment_id
        FROM investments
        WHERE investment_owner = ${Investment_Owner:singlequote}
    )

),

filtered_investment_results AS (
	SELECT 
		*
	FROM results_with_rank
	WHERE  rank = 1
),

refund_per_investment AS (
    SELECT
        ir.investment_id,
        ir.fund_id,
        FUND_VALUE - FUND_INVESTED_MONEY AS "Profit"
    FROM filtered_investment_results ir
    GROUP BY ir.investment_id, ir.fund_id, FUND_VALUE, FUND_INVESTED_MONEY
)


SELECT 
	i.investment_name AS "Investment name",
	f.fund_id AS "Fund ID",
	result_date AS "Quotation date",
	"Profit" AS "Overall profit",
    last_day_result AS "Last day profit",
    last_week_result AS "Last week profit",
    last_month_result AS "Last month profit",
	last_day_result / fund_invested_money * 100 AS "Last day refund",
	last_week_result / fund_invested_money * 100 AS "Last week refund",
	last_month_result / fund_invested_money * 100 AS "Last month refund"
FROM (
SELECT 
	investment_id,
	fund_id,
	SUM("Profit") as "Profit"
FROM refund_per_investment
GROUP BY ROLLUP(investment_id, fund_id)   
) AS ir
INNER JOIN (
    SELECT DISTINCT
        investment_id,
        investment_name
    FROM investments
    WHERE investment_owner = ${Investment_Owner:singlequote}
) AS i ON i.investment_id = ir.investment_id 
LEFT JOIN  filtered_investment_results f ON f.fund_id = ir.fund_id AND f.investment_id = ir.investment_id
WHERE ir.investment_id IS NOT NULL 