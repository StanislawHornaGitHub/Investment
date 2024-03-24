/*
    .DESCRIPTION
        SQL script for PostgreSQL to define INSERT functions in TravelNest DB.

        This file is supposed to define all insert functions,
        which will be used in INSTEAD OF INSERT view triggers.

		Following actions will be performed in a given order:
			1. CREATE OR REPLACE all functions from scratch


    .RULES
		- Names consisted of more than 1 word must use '_' as words separator.
			Object names such as tables, constraints, functions are not case sensitive,
			so to make them easy easy-readable please use word separator.

        - Insert function must have a prefix 'insert_' followed by <view_name> in the name. 
            Because all functions are located in the common Object explorer directory.

        - Insert function must return NULL if operation was successful, 
            otherwise raise an descriptive exception, which will be capture by backend.

        - Insert function can be written in SQL or PL/Python, both languages are supported,
            however RECOMMENDED FOR DATA MODIFICATION IS SQL.

        - Insert function must handle everything related to inserting record to DB,
            including all insert statements to any related table


    .NOTES

        Version:            1.0
        Author:             Stanisław Horna
        Mail:               stanislawhorna@outlook.com
        GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
        Creation Date:      24-Mar-2024
        ChangeLog:

        Date            Who                     What
            
*/

CREATE FUNCTION insert_Fund ()
RETURNS TRIGGER AS $$
DECLARE
    var_fund_url varchar;
    var_fund_name varchar;
    var_fund_id varchar;
    var_category_name varchar;
    var_category_short varchar;
    var_category_id int;
BEGIN

    var_fund_url := NEW.fund_url;

    IF var_fund_url IS NOT NULL THEN
        var_fund_name := get_fund_name(var_fund_url);
        var_fund_id := get_fund_id(var_fund_url);
        var_category_name := get_fund_category(var_fund_url);
        var_category_short := get_fund_category_short(var_fund_url);

        INSERT INTO Fund_Category(c_name, C_shortname)
        VALUES(var_category_name,var_category_short)
        RETURNING ID INTO var_category_id;

        INSERT INTO Fund (ID, F_name, Category_ID, F_url)
        VALUES(var_fund_id,var_fund_name,var_category_id,var_fund_url);

        RETURN NEW;
    END IF;

    RAISE EXCEPTION 'Can not add new fund without URL';

END;
$$ LANGUAGE plpgsql;