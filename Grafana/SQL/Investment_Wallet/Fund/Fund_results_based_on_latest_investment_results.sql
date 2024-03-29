/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display fund results based on latests investment results


    .NOTES

        Version:            1.0
        Author:             Stanisław Horna
        Mail:               stanislawhorna@outlook.com
        GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
        Creation Date:      28-Mar-2024
        ChangeLog:

        Date            Who                     What

*/
WITH selected_owner_investments AS (
    SELECT
        investment_id
    FROM investments
    WHERE investment_owner = ${Investment_Owner:singlequote}
)


SELECT 
    f.fund_id AS "Fund ID",
    fund_name AS "Fund Name",
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
        (last_day_result / fund_invested_money) * 100 AS "Daily refund",
        (last_week_result / fund_invested_money) * 100 AS "Weekly refund",
        (last_month_result / fund_invested_money) * 100 AS "Monthly refund"
    FROM investment_results ir 
    WHERE result_date = (
        SELECT 
            MAX(result_date) 
        FROM investment_results ir2 
        WHERE ir2.investment_id = ir.investment_id
        ) AND investment_id IN (
                SELECT
                    investment_id
                FROM selected_owner_investments
            )
) AS s
LEFT JOIN funds f on f.fund_id = s.fund_id;