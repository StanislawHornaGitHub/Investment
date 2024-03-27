SELECT
    (
        SELECT 
            (SUM(average) * 365)
        FROM(
            SELECT 
                FUND_ID, 
                AVG(LAST_DAY_RESULT) AS "average"  
            FROM INVESTMENT_RESULTS IR 
            GROUP BY FUND_ID 
            )
    ) AS "Refund based on daily data",
    (
        SELECT 
            ((SUM(average)/7) * 365)
        FROM(
            SELECT 
                FUND_ID, 
                AVG(LAST_WEEK_RESULT) AS "average"  
            FROM INVESTMENT_RESULTS IR 
            GROUP BY FUND_ID 
            )
    ) AS "Refund based on weekly data",
    (
        SELECT 
            ((SUM(average)/30) * 365)
        FROM(
            SELECT 
                FUND_ID, 
                AVG(LAST_MONTH_RESULT) AS "average"  
            FROM INVESTMENT_RESULTS IR 
            GROUP BY FUND_ID 
            )
    ) AS "Refund based on monthly data";