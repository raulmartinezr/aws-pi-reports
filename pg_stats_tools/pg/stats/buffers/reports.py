"""SQL Reports module"""

from typing import Any, Dict

import pandas as pd
from rich import print
from rich.panel import Panel
from rich.pretty import Pretty
from tabulate import tabulate

from pg_stats_tools.input_read import read_sql_input
from pg_stats_tools.psql import execute_sql
from pg_stats_tools.pg.stats.reports import Report


class TableCacheHits(Report):
    """
    Standard SQL Report
    """

    def __init__(self, pg_conn_params: Dict[str, Any], **kvargs: Any) -> None:
        self._pg_conn_params = pg_conn_params
        self._command_args = kvargs

    @classmethod
    def get_help(cls) -> str:
        return """
    Buffers: Table buffers hit ratios

        Objective:
            Aim for a cache hit ratio of 99% or higher. This means that 99% of your data accesses are satisfied from the buffer cache, reducing the need to read
            data from disk. A cache hit ratio of 99% is considered “well-engineered”. If it’s significantly less than that, we will need to increase the shared
            buffer cache. As a rule of thumb, you can allocate a significant portion of your available RAM to shared_buffers, but it should not exceed 25-30%
            of your total system RAM.
        Columns:
            - tablename: Name of the table
            - table_cache_hit_ratio_pct: pct of cache hits while reading table data. -1 means no data available (no accesses).
        """

    def get_name(self) -> str:
        return "buffers_table_cache_hits"

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
        help_panel = Panel(self.get_help(), title="Help", height=len(self.get_help().splitlines()) + 1)
        input_panel = Panel(Pretty(self.get_args()), title="Input", height=len(self.get_args()) + 3)

        # layout["Info"]["input"].size=200
        print(help_panel)
        print(input_panel)
        print(tabulate(data, headers="keys", tablefmt=self._command_args["format"]))  # pyright: ignore

    def run(self) -> None:
        data = self.execute_sql()
        self.print(data=data)


class IndexCacheHits(Report):
    """
    Standard SQL Report
    """

    def __init__(self, pg_conn_params: Dict[str, Any], **kvargs: Any) -> None:
        self._pg_conn_params = pg_conn_params
        self._command_args = kvargs

    @classmethod
    def get_help(cls) -> str:
        return """
    Buffers: Index buffers hit ratios

        Objective:
            Aim for a cache hit ratio of 99% or higher. This means that 99% of your data accesses are satisfied from the buffer cache, reducing the need to read
            data from disk. A cache hit ratio of 99% is considered “well-engineered”. If it’s significantly less than that, we will need to increase the shared
            buffer cache. As a rule of thumb, you can allocate a significant portion of your available RAM to shared_buffers, but it should not exceed 25-30%
            of your total system RAM.
        Columns:
            - tablename: Name of the table
            - indexname: Name of the index
            - index_cache_hit_ratio_pct: pct of cache hits while reading indexes. -1 means no data available (no accesses).
        """

    def get_name(self) -> str:
        return "buffers_index_cache_hits"

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
        help_panel = Panel(self.get_help(), title="Help", height=len(self.get_help().splitlines()) + 1)
        input_panel = Panel(Pretty(self.get_args()), title="Input", height=len(self.get_args()) + 3)

        # layout["Info"]["input"].size=200
        print(help_panel)
        print(input_panel)
        print(tabulate(data, headers="keys", tablefmt=self._command_args["format"]))  # pyright: ignore

    def run(self) -> None:
        data = self.execute_sql()
        self.print(data=data)


class Usage(Report):
    """
    Standard SQL Report
    """

    def __init__(self, pg_conn_params: Dict[str, Any], **kvargs: Any) -> None:
        self._pg_conn_params = pg_conn_params
        self._command_args = kvargs

    @classmethod
    def get_help(cls) -> str:
        return """
    Buffers: Usage

        Columns:
            - schema: Schema name (If schema=_all)
            - rel_name: Name of relation (table, sequence, index...)
            - rel_type: Relation type
            - buffer_count: Number of buffers allocated
            - used_buffers: Number of buffers used (pinned at least once by one backend process)
            - used_buffers_pct: pct of used buffers
        """

    def get_name(self) -> str:
        return "buffers_usage"

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
        help_panel = Panel(self.get_help(), title="Help", height=len(self.get_help().splitlines()) + 1)
        input_panel = Panel(Pretty(self.get_args()), title="Input", height=len(self.get_args()) + 3)

        # layout["Info"]["input"].size=200
        print(help_panel)
        print(input_panel)
        print(tabulate(data, headers="keys", tablefmt=self._command_args["format"]))  # pyright: ignore

    def run(self) -> None:
        data = self.execute_sql()
        self.print(data=data)
