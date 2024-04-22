/*
    .DESCRIPTION
        Query for Grafana Dashboard.
        Display current resource consumption (CPU & RAM)


    .NOTES

        Version:            1.0
        Author:             Stanisław Horna
        Mail:               stanislawhorna@outlook.com
        GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment
        Creation Date:      22-Apr-2024
        ChangeLog:

        Date            Who                     What

*/
SELECT
	cpu."CPU normal",
	cpu."CPU niced",
	cpu."CPU kernel",
	ram."RAM usage"
FROM
	(
		SELECT
			ROUND(
				(USED_MEMORY::NUMERIC / TOTAL_MEMORY::NUMERIC) * 100,
				2
			) AS "RAM usage"
		FROM
			PG_SYS_MEMORY_INFO ()
	) AS ram,
	(
		SELECT
			ROUND(USERMODE_NORMAL_PROCESS_PERCENT::NUMERIC, 2) AS "CPU normal",
			ROUND(USERMODE_NICED_PROCESS_PERCENT::NUMERIC, 2) AS "CPU niced",
			ROUND(KERNELMODE_PROCESS_PERCENT::NUMERIC, 2) AS "CPU kernel"
		FROM
			PG_SYS_CPU_USAGE_INFO ()
	) AS cpu;



