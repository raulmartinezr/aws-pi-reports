"""SQL Reports module"""

from typing import Any, Dict, List

import pandas as pd
from rich import print
from rich.panel import Panel
from rich.pretty import Pretty
from tabulate import tabulate

from pg_stats_tools.input_read import read_sql_input
from pg_stats_tools.psql import execute_sql
from pg_stats_tools.pg.stats.reports import Report


class SQLTimeStatsBySQLType(Report):
    """
    Standard SQL Report
    """

    def __init__(self, pg_conn_params: Dict[str, Any], **kvargs: Any) -> None:
        self._pg_conn_params = pg_conn_params
        self._command_args = kvargs

    @classmethod
    def get_help(cls) -> str:
        return """Time statistics for SQL statements grouped by SQL type \n
        Columns:\n
            - sql_type: The type of SQL statement\n
            - avg_time_ms: The average amount of time each SQL statement type took to run, in milliseconds\n
            - num_calls: The number of times each SQL statement type was called\n
            - total_time_ms: The total amount of time each SQL statement type took to run, in milliseconds\n
            - max_time_ms: The maximum amount of time each SQL statement  type took to run, in millisecondsq\n

        """

    def get_name(self) -> str:
        return "sql_time_stats_by_type"

    def get_args(self) -> Dict[str, Any]:
        return self._command_args

    def read_sql(self) -> str:
        return read_sql_input(self.get_name(), **self.get_args())

    def execute_sql(self) -> pd.DataFrame:
        return execute_sql(
            sql=self.read_sql(),
            **self._pg_conn_params,
        )

    def print(self, data: pd.DataFrame) -> None:
        help_panel = Panel(self.get_help(), title="Help", height=len(self.get_help().splitlines()))
        input_panel = Panel(Pretty(self.get_args()), title="Input", height=len(self.get_args()) + 3)

        # layout["Info"]["input"].size=200
        print(help_panel)
        print(input_panel)
        print(tabulate(data, headers="keys", tablefmt=self._command_args["format"]))  # pyright: ignore

    def run(self) -> None:
        data = self.execute_sql()
        self.print(data=data)


class SQLStatsBySQLType(Report):
    """
    Standard SQL Report
    """

    def __init__(self, pg_conn_params: Dict[str, Any], sql_types: Dict[str, str], fetch_fields: List[str], **kvargs: Any) -> None:
        self._pg_conn_params = pg_conn_params
        self._command_args = kvargs
        self._sql_types = sql_types
        self._fetch_fields = fetch_fields

    @classmethod
    def get_help(cls) -> str:
        return """Statistics for SQL statements grouped by SQL type \n
        Columns:\n
            - user: OID of user who executed the statement\n
            - database: Database in which the statement was executed\n
            - queryid:Hash code to identify identical normalized queries.\n
            - query: Text of a representative statement (just first 15 chars displayed)\n
            - calls: Number of times the statement was executed\n
            - total_time: Total time spent executing the statement, in milliseconds\n
            - min_time: Minimum time spent executing the statement, in milliseconds\n
            - max_time: Maximum time spent executing the statement, in milliseconds\n
            - mean_time: Mean time spent executing the statement, in milliseconds\n
            - stddev_time: Population standard deviation of time spent executing the statement, in milliseconds\n
            - rows: Total number of rows retrieved or affected by the statement\n
            - shared_blks_hit: Total number of shared block cache hits by the statement\n
            - shared_blks_read: Total number of shared blocks read by the statement\n
            - shared_blks_dirtied: Total number of shared blocks dirtied by the statementd\n
            - shared_blks_written: Total number of shared blocks written by the statement\n
            - local_blks_hit: Total number of local block cache hits by the statement\n
            - local_blks_read: Total number of local blocks read by the statement\n
            - local_blks_dirtied: Total number of local blocks dirtied by the statement\n
            - local_blks_written: Total number of local blocks written by the statement\n
            - temp_blks_read: Total number of temp blocks read by the statement\n
            - temp_blks_written: Total number of temp blocks written by the statement\n
            - blk_read_time: Total time the statement spent reading data file blocks, in milliseconds (if track_io_timing is enabled, otherwise zero)\n
            - blk_write_time: Number of times the statement was executed\n
        """

    def get_name(self) -> str:
        return "top_sql_stats_by_type"

    def get_args(self) -> Dict[str, Any]:
        return self._command_args

    def read_sql(self, sql_type: str, fetch_fields: List[str]) -> str:
        return read_sql_input(self.get_name(), sql_type=sql_type, fetch_fields=fetch_fields, **self.get_args())

    def execute_sql(self, sql_type: str) -> pd.DataFrame:
        return execute_sql(
            sql=self.read_sql(sql_type=sql_type, fetch_fields=self._fetch_fields),
            **self._pg_conn_params,
        )

    def print_header(self) -> None:
        help_panel = Panel(self.get_help(), title="Help", height=len(self.get_help().splitlines()))
        input_panel = Panel(Pretty(f"Args: {self._command_args}\n{self._sql_types}"), title="Input", height=len(self.get_args()) + 3)
        print(help_panel)
        print(input_panel)

    def print_data(self, sql_type: str, data: pd.DataFrame) -> None:
        print("-" * 50)
        print(f"SQL Type: {sql_type}")
        print(tabulate(data, headers="keys", tablefmt=self._command_args["format"]))  # pyright: ignore

    def run(self) -> None:
        self.print_header()
        for k, v in self._sql_types.items():
            data = self.execute_sql(sql_type=v)
            self.print_data(sql_type=k, data=data)


class ActiveLongRunningSQL(Report):
    """
    Standard SQL Report
    """

    def __init__(self, pg_conn_params: Dict[str, Any], sql_types: Dict[str, str], fetch_fields: List[str], **kvargs: Any) -> None:
        self._pg_conn_params = pg_conn_params
        self._command_args = kvargs
        self._sql_types = sql_types
        self._fetch_fields = fetch_fields

    @classmethod
    def get_help(cls) -> str:
        return """Active long running SQL queries \n
        Columns:\n
        - datid: OID of the database this backend is connected to

        - datname: Name of the database this backend is connected to

        - pid: Process ID of this backend

        - leader_pid: Process ID of the parallel group leader, if this process is a parallel query worker. NULL if this process is a parallel group leader or does not participate in parallel query.

        - usesysid: OID of the user logged into this backend

        - usename: Name of the user logged into this backend

        - application_name: Name of the application that is connected to this backend

        - client_addr: IP address of the client connected to this backend. If this field is null, it indicates either that the client is connected via a Unix socket on the server machine or that this is an internal process such as autovacuum.

        - client_hostname: Host name of the connected client, as reported by a reverse DNS lookup of client_addr. This field will only be non-null for IP connections, and only when log_hostname is enabled.

        - client_port: TCP port number that the client is using for communication with this backend, or -1 if a Unix socket is used. If this field is null, it indicates that this is an internal server process.

        - backend_start: Time when this process was started. For client backends, this is the time the client connected to the server.

        - xact_start: Time when this process' current transaction was started, or null if no transaction is active. If the current query is the first of its transaction, this column is equal to the query_start column.

        - query_start: Time when the currently active query was started, or if state is not active, when the last query was started

        - state_change: Time when the state was last changed

        - wait_event_type: The type of event for which the backend is waiting, if any; otherwise NULL. See Table 28.4.

        - wait_event: Wait event name if backend is currently waiting, otherwise NULL. See Table 28.5 through Table 28.13.

        - state: Current overall state of this backend. Possible values are:

        - active: The backend is executing a query.

        - idle: The backend is waiting for a new client command.

        - idle in transaction: The backend is in a transaction, but is not currently executing a query.

        - idle in transaction (aborted): This state is similar to idle in transaction, except one of the statements in the transaction caused an error.

        - fastpath function call: The backend is executing a fast-path function.

        - disabled: This state is reported if track_activities is disabled in this backend.

        - backend_xid: Top-level transaction identifier of this backend, if any.

        - backend_xmin: The current backend's xmin horizon.

        - query_id: Identifier of this backend's most recent query. If state is active this field shows the identifier of the currently executing query. In all other states, it shows the identifier of last query that was executed. Query identifiers are not computed by default so this field will be null unless compute_query_id parameter is enabled or a third-party module that computes query identifiers is configured.

        - query: Text of this backend's most recent query. If state is active this field shows the currently executing query. In all other states, it shows the last query that was executed. By default the query text is truncated at 1024 bytes; this value can be changed via the parameter track_activity_query_size.

        - backend_type: Type of current backend. Possible types are autovacuum launcher, autovacuum worker, logical replication launcher, logical replication worker, parallel worker, background writer, client backend, checkpointer, archiver, startup, walreceiver, walsender and walwriter. In addition, background workers registered by extensions may have additional types.
        """

    def get_name(self) -> str:
        return "active_sql_long_running"

    def get_args(self) -> Dict[str, Any]:
        return self._command_args

    def read_sql(self, sql_type: str, fetch_fields: List[str]) -> str:
        return read_sql_input(self.get_name(), sql_type=sql_type, fetch_fields=fetch_fields, **self.get_args())

    def execute_sql(self, sql_type: str) -> pd.DataFrame:
        return execute_sql(
            sql=self.read_sql(sql_type=sql_type, fetch_fields=self._fetch_fields),
            **self._pg_conn_params,
        )

    def print_header(self) -> None:
        help_panel = Panel(self.get_help(), title="Help", height=len(self.get_help().splitlines()))
        input_panel = Panel(Pretty(f"Args: {self._command_args}\n{self._sql_types}"), title="Input", height=len(self.get_args()) + 3)
        print(help_panel)
        print(input_panel)

    def print_data(self, sql_type: str, data: pd.DataFrame) -> None:
        print("-" * 50)
        print(f"SQL Type: {sql_type}")
        print(tabulate(data, headers="keys", tablefmt=self._command_args["format"]))  # pyright: ignore

    def run(self) -> None:
        self.print_header()
        for k, v in self._sql_types.items():
            data = self.execute_sql(sql_type=v)
            self.print_data(sql_type=k, data=data)
