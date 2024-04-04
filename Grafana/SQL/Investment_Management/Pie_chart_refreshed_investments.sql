/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display pie chart of refreshed investment results


    .NOTES

        Version:            1.0
        Author:             Stanisław Horna
        Mail:               stanislawhorna@outlook.com
        GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
        Creation Date:      04-Apr-2024
        ChangeLog:

        Date            Who                     What

*/

WITH last_investment_date AS (
    SELECT 
        MAX(result_date) as "last_result_date"
    FROM investment_results
),

refreshed_investments AS (
    SELECT
        COUNT(*) AS "Refreshed"
    FROM (
        SELECT DISTINCT
            investment_id
        FROM investment_results
        WHERE result_date = (
            SELECT 
                last_result_date
            FROM last_investment_date
        )
    ) AS i
    WHERE
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
                    result_date = (
                        SELECT 
                            last_result_date
                        FROM last_investment_date
                    )
            )
        )
),

all_investments AS (
    SELECT
        COUNT(*) AS "All investments"
    FROM (
        SELECT DISTINCT
            investment_id
        FROM investments
    )
)

SELECT
    "Refreshed",
    ("All investments" - "Refreshed") AS "Not refreshed"
FROM refreshed_investments, all_investments

