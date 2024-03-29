/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display table with fund operations


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
    OPERATION_QUOTATION_DATE AS "Date",
    FUND_NAME AS "Fund name",
    f.FUND_ID AS "Fund ID",
    operation_value AS "Money"
FROM INVESTMENTS I 
LEFT JOIN FUNDS F ON f.FUND_ID = i.INVESTMENT_FUND_ID
WHERE investment_owner = ${Investment_Owner:singlequote};