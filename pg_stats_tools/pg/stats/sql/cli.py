"""SQL module"""


from enum import Enum
from typing import Annotated, Any, Dict, List, Union

import typer

from pg_stats_tools.format import TableFormatOption
from pg_stats_tools.pg.cli import pg_params
from pg_stats_tools.pg.stats.sql.reports import SQLStatsBySQLType, SQLTimeStatsBySQLType

sql = typer.Typer(
    help="""Performance reports for SQL statements based on pg_stat_statements
    """
)


class SqlTimeStatsFields(str, Enum):
    avg_time_ms = "avg_time_ms"
    num_calls = "num_calls"
    total_time_ms = "total_time_ms"
    max_time_ms = "max_time_ms"


class SQLStatsFields(str, Enum):
    calls = "calls"
    total_time = "total_time"
    min_time = "min_time"
    max_time = "max_time"
    mean_time = "mean_time"
    stddev_time = "stddev_time"
    rows = "rows"
    shared_blks_hit = "shared_blks_hit"
    shared_blks_read = "shared_blks_read"
    shared_blks_dirtied = "shared_blks_dirtied"
    shared_blks_written = "shared_blks_written"
    local_blks_hit = "local_blks_hit"
    local_blks_read = "local_blks_read"
    local_blks_dirtied = "local_blks_dirtied"
    local_blks_written = "local_blks_written"
    temp_blks_read = "temp_blks_read"
    temp_blks_written = "temp_blks_written"
    blk_read_time = "blk_read_time"
    blk_write_time = "blk_write_time"


class SQLTypes(str, Enum):
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    FETCH = "FETCH"
    CREATE = "CREATE"
    DROP = "DROP"
    ALTER = "ALTER"
    TRUNCATE = "TRUNCATE"
    GRANT = "GRANT"
    REVOKE = "REVOKE"
    MOVE = "MOVE"
    COMMIT = "COMMIT"
    ROLLBACK = "ROLLBACK"
    SAVEPOINT = "SAVEPOINT"
    TRANSACTION = "BEGIN"


@sql.command(help=SQLStatsBySQLType.get_help())
def sql_time_stats_by_type(
    order_by: Annotated[
        SqlTimeStatsFields,
        typer.Option(
            help="Field used to specify the order in which the result set should be sorted",
            case_sensitive=True,
        ),
    ] = SqlTimeStatsFields.avg_time_ms,
    format: Annotated[
        TableFormatOption,
        typer.Option(help="Output table format", case_sensitive=True),
    ] = TableFormatOption.psql,
    dbid: Annotated[
        str,
        typer.Option(help="Database name"),
    ] = "_all",
) -> None:
    # frame: Union[FrameType, None] = inspect.currentframe()
    # f_name = frame.f_code.co_name if frame else "unknown_function"

    command_args: Dict[str, Any] = {
        "order_by": order_by.value,
        "format": format.value,
        "dbid": dbid,
    }

    SQLTimeStatsBySQLType(pg_conn_params=pg_params, **command_args).run()


@sql.command(help=SQLStatsBySQLType.get_help())
def top_sql_stats_by_type(
    top_stat_field: Annotated[
        SQLStatsFields,
        typer.Option(
            help="Fielt to use to obtain expensive SQL statements",
            case_sensitive=True,
        ),
    ] = SQLStatsFields.mean_time,
    format: Annotated[
        TableFormatOption,
        typer.Option(help="Output table format", case_sensitive=True),
    ] = TableFormatOption.grid,
    dbid: Annotated[
        str,
        typer.Option(help="Database name"),
    ] = "_all",
    count: Annotated[
        int,
        typer.Option(help="Number of SQL to fecth (for each SQL type)"),
    ] = 10,
    fetch_field: Annotated[
        Union[List[SQLStatsFields], None],
        typer.Option(help="Additional field to be fechted"),
    ] = None,
    sql_type: Annotated[
        Union[List[SQLTypes], None],
        typer.Option(help="SQL Types"),
    ] = None,
) -> None:
    # frame: Union[FrameType, None] = inspect.currentframe()
    # f_name = frame.f_code.co_name if frame else "unknown_function"
    if not sql_type:
        sql_type = [SQLTypes.SELECT, SQLTypes.INSERT, SQLTypes.UPDATE, SQLTypes.DELETE]
    if not fetch_field:
        fetch_field = [SQLStatsFields.rows, SQLStatsFields.calls, SQLStatsFields.total_time, SQLStatsFields.mean_time]
    command_args: Dict[str, Any] = {
        "top_stat_field": top_stat_field.value,
        "format": format.value,
        "dbid": dbid,
        "count": count,
    }
    sql_types = {sql_type.name: sql_type.value for sql_type in sql_type}
    fetch_fields = [field.name for field in fetch_field if field != top_stat_field]
    SQLStatsBySQLType(pg_conn_params=pg_params, sql_types=sql_types, fetch_fields=fetch_fields, **command_args).run()
