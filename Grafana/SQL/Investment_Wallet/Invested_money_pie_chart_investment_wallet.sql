/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display pie chart of product participation in whole wallet.


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
    investment_name,
    SUM(operation_value)
FROM investments i
WHERE investment_owner = ${Investment_Owner:singlequote}
GROUP BY investment_name;