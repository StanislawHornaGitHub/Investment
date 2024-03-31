/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display fund results based on latests investment results


    .NOTES

        Version:            1.1
        Author:             Stanisław Horna
        Mail:               stanislawhorna@outlook.com
        GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
        Creation Date:      28-Mar-2024
        ChangeLog:

        Date            Who                     What
        2024-03-31      Stanisław Horna         Moved from max date to row_number function
*/

WITH selected_owner_investments AS (
    SELECT DISTINCT
        investment_id
    FROM investments
    WHERE investment_owner = ${Investment_Owner:singlequote}
),
investment_results_with_rank AS (
    SELECT
        *,
        ROW_NUMBER () OVER (PARTITION BY fund_id, investment_id ORDER BY result_date DESC) as "rank"
    FROM investment_results
),

latest_investment_results AS (
    SELECT
        *
    FROM investment_results_with_rank
    WHERE "rank" = 1
)


SELECT 
    f.fund_id AS "Fund ID",
    fund_name AS "Fund Name",
    "Overall refund",
    "Daily refund",
    "Weekly refund",
    "Monthly refund",
    CASE 
        WHEN "Monthly refund" is not NULL  THEN ("Monthly refund"/30) * 365
        WHEN "Weekly refund" is not NULL THEN ("Weekly refund"/7) * 365
        WHEN "Daily refund" is not NULL THEN ("Daily refund") * 365
    END AS "Estimated yearly refund"
FROM (
    SELECT 
        FUND_ID,
        ((fund_value / fund_invested_money) -1) * 100 as "Overall refund",
        (last_day_result / fund_invested_money) * 100 AS "Daily refund",
        (last_week_result / fund_invested_money) * 100 AS "Weekly refund",
        (last_month_result / fund_invested_money) * 100 AS "Monthly refund"
    FROM latest_investment_results
    WHERE investment_id IN (
                SELECT
                    investment_id
                FROM selected_owner_investments
            )
) AS s
LEFT JOIN funds f on f.fund_id = s.fund_id;