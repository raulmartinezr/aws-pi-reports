-- Executed for each sql_type
SELECT
    usename AS username,
    datname AS database,
    LEFT(query, 15) AS query,
    age(clock_timestamp(), query_start) as time_running
    {% for fetch_field in fetch_fields %}
    , {{fetch_field}}
    {% endfor %}
FROM pg_stat_activity
-- JOIN pg_catalog.pg_stat_statements.queryid ON pg_catalog.pg_stat_statements.query = pg_stat_activity.query and  pg_catalog.pg_stat_statements.backend_start = pg_stat_activity.backend_start
WHERE
    pg_stat_activity.pid != pg_backend_pid()
    AND state != 'idle'
    {% if dbname !="_all" %}
    AND database = {{dbname}}
    {% endif %}
    AND query ~* '.*{{sql_type}}.*'


ORDER BY time_running DESC
LIMIT {{count}};