WITH table_scans as (
    SELECT relid,
        tables.idx_scan + tables.seq_scan as all_scans,
        ( tables.n_tup_ins + tables.n_tup_upd + tables.n_tup_del ) as writes,
                pg_relation_size(relid) as table_size
        FROM pg_stat_user_tables as tables
        {% if schema !="_all" %} WHERE  tables.schemaname='{{schema}}' {% endif %}
),
all_writes as (
    SELECT sum(writes) as total_writes
    FROM table_scans
),
indexes as (
    SELECT idx_stat.relid, idx_stat.indexrelid,
        idx_stat.schemaname, idx_stat.relname as tablename,
        idx_stat.indexrelname as indexname,
        idx_stat.idx_scan,
        pg_relation_size(idx_stat.indexrelid) as index_bytes,
        CASE
            WHEN indexdef ~* 'USING btree' THEN 'BTREE'
            WHEN indexdef ~* 'USING hash' THEN 'HASH'
            WHEN indexdef ~* 'USING gist' THEN 'GIST'
            WHEN indexdef ~* 'USING spgist' THEN 'SPGIST'
            WHEN indexdef ~* 'USING gin' THEN 'GIN'
            WHEN indexdef ~* 'USING brin' THEN 'BRIN'
            WHEN indexdef ~* 'USING bloom' THEN 'BLOOM'
            ELSE 'OTHER'
        END AS idx_type
    FROM pg_stat_user_indexes as idx_stat
        JOIN pg_index
            USING (indexrelid)
        JOIN pg_indexes as indexes
            ON idx_stat.schemaname = indexes.schemaname
                AND idx_stat.relname = indexes.tablename
                AND idx_stat.indexrelname = indexes.indexname
    WHERE pg_index.indisunique = FALSE
    {% if schema !="_all" %} AND  idx_stat.schemaname='{{schema}}' {% endif %}
),
index_ratios AS (
SELECT tablename, indexname,
    idx_scan, all_scans,
    round(( CASE WHEN all_scans = 0 THEN 0.0::NUMERIC
        ELSE idx_scan::NUMERIC/all_scans * 100 END),2) as idx_scan_pct,
    writes,
    round((CASE WHEN writes = 0 THEN -1 ELSE idx_scan::NUMERIC/writes  END),2)
        as scans_per_write,
    pg_size_pretty(index_bytes) as idx_size,
    pg_size_pretty(table_size) as tbl_size,
    idx_type
    FROM indexes
    JOIN table_scans
    USING (relid)
)

SELECT * FROM index_ratios;