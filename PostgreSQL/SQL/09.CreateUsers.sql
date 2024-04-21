/*
    .DESCRIPTION
        SQL script for PostgreSQL to CREATE users in Investments DB.

        Users to be created:
            - api_read <- will have access to SELECT views only.
            - api_write <- will have access to INSERT and UPDATE views only.
            - grafana_read <- will have access to SELECT views and invoke grafana functions.

    .NOTES

        Version:            1.0
        Author:             Stanisław Horna
        Mail:               stanislawhorna@outlook.com
        GitHub Repository:  https://github.com/PLProjektKompetencyjny/PK_6IO1z_Projekt4_DataBase
        Creation Date:      19-Apr-2024
        ChangeLog:

        Date            Who                     What

*/

-- create required roles
CREATE ROLE "api_read" LOGIN PASSWORD 'inv!r_ap_ead1';
CREATE ROLE "api_write" LOGIN PASSWORD 'inv!w_ap_ite2';
CREATE ROLE "grafana_read" LOGIN PASSWORD 'inv!w_gf_ead3';


-- Grant privileges for API READ user
GRANT CONNECT ON DATABASE "Investments" to "api_read";
GRANT USAGE ON SCHEMA public TO "api_read";
GRANT SELECT ON funds to "api_read";
GRANT SELECT ON investment_results to "api_read";
GRANT SELECT ON investments to "api_read";
GRANT SELECT ON quotations to "api_read";


-- Grant privileges for API WRITE user
GRANT CONNECT ON DATABASE "Investments" to "api_write";
GRANT USAGE ON SCHEMA public TO "api_write";
GRANT SELECT, INSERT, UPDATE ON funds to "api_write";
GRANT SELECT, INSERT, UPDATE ON investment_results to "api_write";
GRANT SELECT, INSERT, UPDATE ON investments to "api_write";
GRANT SELECT, INSERT, UPDATE ON quotations to "api_write";

-- Grant privileges for Grafana user
GRANT CONNECT ON DATABASE "Investments" to "grafana_read";
GRANT USAGE ON SCHEMA public TO "grafana_read";
GRANT SELECT ON funds to "grafana_read";
GRANT SELECT ON investment_results to "grafana_read";
GRANT SELECT ON investments to "grafana_read";
GRANT SELECT ON quotations to "grafana_read";

GRANT EXECUTE ON FUNCTION get_funds_quotation(varchar, varchar) to "grafana_read";
GRANT EXECUTE ON FUNCTION get_investments_result(varchar, varchar) to "grafana_read";
GRANT EXECUTE ON FUNCTION remove_investments_result() to "grafana_read";
GRANT EXECUTE ON FUNCTION remove_fund_quotation() to "grafana_read";