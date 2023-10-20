SELECT
  {% if schema =="_all" %} schemaname AS schemaname,{% endif %}
  relname AS tablename,
  indexrelname AS indexname,
  CASE
  	WHEN (
		SUM(idx_blks_hit) + SUM(idx_blks_read)) = 0 THEN -1::NUMERIC
        ELSE round(SUM(idx_blks_hit)::NUMERIC/(SUM(idx_blks_hit) + SUM(idx_blks_read)) * 100,2)
	END AS idx_cache_hit_ratio_pct
FROM pg_statio_all_indexes
{% if schema !="_all" %} WHERE schemaname='{{schema}}' {% endif %}
GROUP BY relname,indexrelname{% if schema =="_all" %},schemaname{% endif %}
ORDER BY idx_cache_hit_ratio_pct DESC
