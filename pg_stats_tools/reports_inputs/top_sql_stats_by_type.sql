-- Executed for each sql_type
SELECT
    pg_user.usename AS user,
    {% if dbname =="_all" %} pg_stat_database.datname AS database,{% endif %}
    queryid,
    LEFT(query, 50) AS query,
    {{top_stat_field}}
    {% for fetch_field in fetch_fields %}
    , {{fetch_field}}
    {% endfor %}
FROM pg_stat_statements
JOIN pg_catalog.pg_user ON pg_stat_statements.userid = pg_catalog.pg_user.usesysid
JOIN pg_stat_database ON pg_stat_statements.dbid = pg_stat_database.datid
WHERE
    query ~*  '^\s*{{sql_type}}'
{% if dbname !="_all" %}
    AND pg_stat_database.datname = {{database}}
{% endif %}
ORDER BY {{top_stat_field}} DESC
LIMIT {{count}};