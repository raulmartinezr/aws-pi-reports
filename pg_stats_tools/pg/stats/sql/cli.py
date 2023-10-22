"""SQL module"""


from enum import Enum
from typing import Annotated, Any, Dict, List, Union
from datetime import datetime, timedelta

import typer

from pg_stats_tools.time_fn import parse_timestamp
from pg_stats_tools.format import TableFormatOption
from pg_stats_tools.pg.cli import pg_params
from pg_stats_tools.pg.stats.sql.reports import SQLStatsBySQLType, SQLTimeStatsBySQLType, ActiveLongRunningSQL, SQLStatsSimplifiedBySQLType

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


# https://documentation.red-gate.com/sm13/postgresql-top-queries-199098901.html
class SQLSimplifiedStatsFields(str, Enum):
    calls = "calls"
    rows = "rows"
    arows = "arows"
    time = "time"
    atime = "atime"
    iotime = "iotime"
    aiotime = "aiotime"
    blk_r = "blk_r"
    ablk_r = "ablk_r"
    buff_blk_r = "buff_blk_r"
    abuff_blk_r = "abuff_blk_r"
    buff_blk_r_pct = "buff_blk_r_pct"
    blk_w = "blk_w"
    ablk_w = "ablk_w"


class ActiveSQLStatsFields(str, Enum):
    application_name = "application_name"
    client_addr = "client_addr"
    client_hostname = "client_hostname"
    client_port = "client_port"
    backend_start = "backend_start"
    xact_start = "xact_start"
    query_start = "query_start"
    state_change = "state_change"
    wait_event_type = "wait_event_type"
    wait_event = "wait_event"
    state = "state"
    backend_xid = "backend_xid"
    backend_xmin = "backend_xmin"
    query = "query"
    backend_type = "backend_type"


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


class SortDir(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


@sql.command(help=SQLTimeStatsBySQLType.get_help())
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
    ] = TableFormatOption.github,
    dbname: Annotated[
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
        "dbname": dbname,
        "count": count,
    }
    sql_types = {sql_type.name: sql_type.value for sql_type in sql_type}
    fetch_fields = [field.name for field in fetch_field if field != top_stat_field]
    SQLStatsBySQLType(pg_conn_params=pg_params, sql_types=sql_types, fetch_fields=fetch_fields, **command_args).run()


@sql.command(help=SQLStatsSimplifiedBySQLType.get_help())
def top_sql_stats_simplified_by_type(
    top_stat_field: Annotated[
        SQLSimplifiedStatsFields,
        typer.Option(
            help="Fielt to use to obtain expensive SQL statements",
            case_sensitive=True,
        ),
    ] = SQLSimplifiedStatsFields.atime,
    format: Annotated[
        TableFormatOption,
        typer.Option(help="Output table format", case_sensitive=True),
    ] = TableFormatOption.github,
    dbname: Annotated[
        str,
        typer.Option(help="Database name"),
    ] = "_all",
    count: Annotated[
        int,
        typer.Option(help="Number of SQL to fecth (for each SQL type)"),
    ] = 10,
    sort: Annotated[
        SortDir,
        typer.Option(help="Sort direction. Defines the relevance of high/low values for top_stat_field"),
    ] = SortDir.DESC,
    sql_type: Annotated[
        List[SQLTypes],
        typer.Option(help="SQL Types"),
    ] = [SQLTypes.SELECT, SQLTypes.INSERT, SQLTypes.UPDATE, SQLTypes.DELETE],
) -> None:
    # frame: Union[FrameType, None] = inspect.currentframe()
    # f_name = frame.f_code.co_name if frame else "unknown_function"
    command_args: Dict[str, Any] = {"top_stat_field": top_stat_field.value, "sort": sort.value, "format": format.value, "dbname": dbname, "count": count}
    sql_types = {sql_type.name: sql_type.value for sql_type in sql_type}
    SQLStatsSimplifiedBySQLType(pg_conn_params=pg_params, sql_types=sql_types, **command_args).run()


@sql.command(help=ActiveLongRunningSQL.get_help())
def active_sql_long_running(
    format: Annotated[
        TableFormatOption,
        typer.Option(help="Output table format", case_sensitive=True),
    ] = TableFormatOption.github,
    dbname: Annotated[
        str,
        typer.Option(help="Database name"),
    ] = "_all",
    count: Annotated[
        int,
        typer.Option(help="Number of SQL to fecth (for each SQL type)"),
    ] = 10,
    fetch_field: Annotated[
        Union[List[ActiveSQLStatsFields], None],
        typer.Option(help="Additional field to be fechted"),
    ] = None,
    sql_type: Annotated[
        List[SQLTypes],
        typer.Option(help="SQL Types"),
    ] = [SQLTypes.SELECT, SQLTypes.INSERT, SQLTypes.UPDATE, SQLTypes.DELETE],
) -> None:
    # frame: Union[FrameType, None] = inspect.currentframe()
    # f_name = frame.f_code.co_name if frame else "unknown_function"
    if not fetch_field:
        fetch_field = [
            ActiveSQLStatsFields.application_name,
            ActiveSQLStatsFields.client_addr,
            ActiveSQLStatsFields.client_hostname,
            ActiveSQLStatsFields.wait_event,
            ActiveSQLStatsFields.state,
        ]
    command_args: Dict[str, Any] = {
        "format": format.value,
        "dbname": dbname,
        "count": count,
    }
    sql_types = {sql_type.name: sql_type.value for sql_type in sql_type}
    fetch_fields = [field.name for field in fetch_field]
    ActiveLongRunningSQL(pg_conn_params=pg_params, sql_types=sql_types, fetch_fields=fetch_fields, **command_args).run()
