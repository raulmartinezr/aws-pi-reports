"""SQL Reports module"""

import pandas as pd
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Union

from rich import print
from rich.panel import Panel
from rich.pretty import Pretty
from tabulate import tabulate

from pg_stats_tools.input_read import read_sql_input
from pg_stats_tools.psql import execute_sql


class Report(ABC):
    """
    Interface for all reports
    """

    # @property
    # @abstractmethod
    # def product(self) -> None:
    #     pass
    @classmethod
    @abstractmethod
    def get_help(cls) -> str:
        pass

    @abstractmethod
    def run(self) -> None:
        pass


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
        help_panel = Panel(self.get_help(), title="Help", height=self.get_help().count("\n"))
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
        return """Time statistics for SQL statements grouped by SQL type \n
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
        help_panel = Panel(self.get_help(), title="Help", height=self.get_help().count("\n"))
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
