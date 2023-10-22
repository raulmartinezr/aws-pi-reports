CREATE OR REPLACE FUNCTION add_decimals_if_present(input_number numeric, decimals int)
RETURNS numeric AS $$
BEGIN
    IF input_number = trunc(input_number) THEN
        RETURN trunc(input_number); -- No decimals, return as-is
    ELSE
        RETURN round(input_number::numeric, decimals::int); -- Round to specified number of decimals
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION format_large_number(input_number numeric)
RETURNS text AS $$
DECLARE
    units text[] := ARRAY['','k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'];
    result text;
    unit_index int := 1;
BEGIN
    WHILE input_number >= 1000.0 AND unit_index < array_length(units, 1) LOOP
        input_number := input_number / 1000.0;
        unit_index := unit_index + 1;
    END LOOP;

    result := add_decimals_if_present(input_number::numeric, 2)::text || units[unit_index];
    RETURN result;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION format_duration(milliseconds float)
RETURNS text AS $$
DECLARE
    units text[] := ARRAY['ms', 's', 'm', 'h', 'd'];
    unit_names text[] := ARRAY['', 's', 'm', 'h', 'd'];
    conversion_factors numeric[] := ARRAY[1000, 60, 60, 24];
    result text;
    unit_index int := 1;
BEGIN
    FOR i IN 1..array_length(conversion_factors, 1) LOOP
        EXIT WHEN  milliseconds < conversion_factors[i] OR unit_index >= array_length(units, 1);
        milliseconds := milliseconds / conversion_factors[i];
        unit_index := unit_index + 1;
    END LOOP;
    result := ROUND(milliseconds::numeric,2) || ' ' || unit_names[unit_index];
    RETURN result;
END;
$$ LANGUAGE plpgsql;



WITH data as (
	SELECT
		pg_user.usename AS user,
        {% if dbname =="_all" %} pg_database.datname AS database,{% endif %}
		queryid AS queryid,
		calls AS calls,
		rows AS rows,
		total_time as time,
		ROUND(total_time::numeric / calls::numeric, 2)  AS atime,
		(pgss.blk_read_time + pgss.blk_write_time) AS iotime,
		(shared_blks_read+local_blks_read+temp_blks_read) AS blk_read,
		(shared_blks_hit+local_blks_hit) AS buff_blk_read,
	    (shared_blks_written + local_blks_written + temp_blks_written)  AS blk_written

	FROM pg_stat_statements as pgss
	LEFT JOIN pg_catalog.pg_user ON pgss.userid = pg_catalog.pg_user.usesysid
	LEFT JOIN pg_database ON pgss.dbid = 	pg_database.oid
	WHERE
        query ~*  '^\s*{{sql_type}}'
        {% if dbname !="_all" %}
            AND pg_database.datname = {{database}}
        {% endif %}
    ORDER BY {{top_stat_field}} {{sort}}
    LIMIT {{count}}
)
SELECT
	data.user AS user,
    {% if dbname =="_all" %} data.database AS database,{% endif %}
    data.queryid AS queryid,
    data.calls AS calls,
    format_large_number(data.rows) AS rows,
	format_large_number(add_decimals_if_present(data.rows::numeric / data.calls,2))  AS arows,
    format_duration(data.time) as time,
    data.atime AS atime,
    format_duration(data.iotime) AS iotime,
	add_decimals_if_present(data.iotime::numeric/data.calls::numeric,2) AS aiotime,
    format_large_number(data.blk_read) AS blk_r,
	 format_large_number(add_decimals_if_present(data.blk_read/data.calls,2)) AS ablk_r,
    format_large_number(data.buff_blk_read) AS buff_blk_r,
    format_large_number(add_decimals_if_present(data.buff_blk_read/calls,2)) AS abuff_blk_r,
	CASE
		WHEN (data.buff_blk_read + data.blk_read) = 0 THEN -1::NUMERIC
		ELSE ROUND(data.buff_blk_read::numeric/(data.buff_blk_read + data.blk_read)*100,2)
	END AS buff_blk_read_pct,
	format_large_number(data.blk_written) AS blk_w,
	format_large_number(add_decimals_if_present(data.blk_written/calls,2))  AS ablk_w
FROM data
