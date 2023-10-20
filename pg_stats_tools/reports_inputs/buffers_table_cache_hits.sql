SELECT
  {% if schema =="_all" %} schemaname as schemaname, {% endif %}
  relname as tablename,
  round(
        ( CASE
            WHEN (SUM(heap_blks_hit) + SUM(heap_blks_read)) = 0 THEN -1::NUMERIC
            ELSE SUM(heap_blks_hit)::NUMERIC/(SUM(heap_blks_hit) + SUM(heap_blks_read)) * 100
         END)
    ,2) as table_cache_hit_ratio_pct
FROM  pg_statio_all_tables
{% if schema !="_all" %} WHERE schemaname='{{schema}}' {% endif %}
GROUP BY relname {% if schema =="_all" %} ,schemaname {% endif %}
ORDER BY table_cache_hit_ratio_pct DESC