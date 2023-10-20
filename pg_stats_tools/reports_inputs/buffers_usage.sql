SELECT
	{% if schema =="_all" %}n.nspname AS sch_name,{% endif %}
	c.relname AS rel_name,
	CASE
    	WHEN c.relkind = 'r' THEN 'ordinary table'
		WHEN c.relkind = 'i' THEN 'index'
		WHEN c.relkind = 'S' THEN 'sequence'
		WHEN c.relkind = 't' THEN 'TOAST table'
		WHEN c.relkind = 'v' THEN 'view'
		WHEN c.relkind = 'm' THEN 'materialized view'
		WHEN c.relkind = 'c' THEN 'composite type'
		WHEN c.relkind = 'f' THEN 'foreign table'
		WHEN c.relkind = 'p' THEN 'partitioned table'
		WHEN c.relkind = 'I' THEN 'partitioned index'
     END AS rel_type,
	 count(*) AS buffer_count,
	 SUM(CASE WHEN usagecount > 0 THEN 1 ELSE 0 END) AS used_buffers,
	 SUM(CASE WHEN usagecount > 0 THEN 1 ELSE 0 END)/count(*)*100 as used_buffers_pct
FROM pg_buffercache b
LEFT JOIN pg_class c ON b.relfilenode = pg_relation_filenode(c.oid)
	AND b.reldatabase IN (0, (SELECT oid FROM pg_database WHERE datname = current_database()))
LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
{% if schema !="_all" %} WHERE n.nspname='{{schema}}' {% endif %}
GROUP BY sch_name, c.relname,c.relkind{% if schema =="_all" %},n.nspname{% endif %}
ORDER BY used_buffers_pct DESC