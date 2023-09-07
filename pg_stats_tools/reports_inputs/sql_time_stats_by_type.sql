WITH TEMP AS (
    SELECT
        CASE
            WHEN query ILIKE '%SELECT%' THEN 'SELECT' -- DQL
            WHEN query ILIKE '%FETCH%' THEN 'FETCH' -- DQL
            WHEN query ILIKE '%INSERT%' THEN 'INSERT' -- DML
            WHEN query ILIKE '%UPDATE%' THEN 'UPDATE' -- DML
            WHEN query ILIKE '%DELETE%' THEN 'DELETE' -- DML
            WHEN query ILIKE '%CREATE%' THEN 'CREATE' -- DDL
            WHEN query ILIKE '%DROP%' THEN 'DROP' -- DDL
            WHEN query ILIKE '%ALTER%' THEN 'ALTER' -- DDL
            WHEN query ILIKE '%TRUNCATE%' THEN 'TRUNCATE' -- DDL
            WHEN query ILIKE '%GRANT%' THEN 'GRANT' -- DCL
            WHEN query ILIKE '%REVOKE%' THEN 'REVOKE' -- DCL
            WHEN query ILIKE '%MOVE%' THEN 'MOVE'
            WHEN query ILIKE '%COMMIT%' THEN 'COMMIT' -- TCL
            WHEN query ILIKE '%ROLLBACK%' THEN 'ROLLBACK' -- TCL
            WHEN query ILIKE '%SAVEPOINT%' THEN 'SAVEPOINT' -- TCL
            WHEN query ILIKE '%BEGIN%' THEN 'TRANSACTION'
            ELSE 'OTHER'
        END AS sql_type,
        COUNT(*) AS num_calls
        {% if dbid !="_all" %},pg_stat_database.datname AS database{% endif %}
        ,SUM(total_time) AS total_time_ms,
	    MAX(total_time) AS max_time_ms,
		MIN(total_time) AS min_time_ms
    FROM pg_stat_statements
    {% if dbid !="_all" %}JOIN pg_stat_database ON pg_stat_statements.dbid = pg_stat_database.datid{% endif %}
    {% if dbid !="_all" %}WHERE pg_stat_statements.dbid = {{dbid}}{% endif %}
    GROUP BY sql_type{% if dbid !="_all" %},pg_stat_database.datname{% endif %}

)
SELECT
    sql_type
    {% if dbid !="_all" %}, database{% endif %}
    ,num_calls,
    ROUND(total_time_ms::numeric, 0) as total_time_ms,
    (total_time_ms / num_calls)::integer AS avg_time_ms,
	 ROUND(max_time_ms::numeric, 0) as max_time_ms,
	min_time_ms
FROM TEMP
ORDER BY {{order_by}} DESC;