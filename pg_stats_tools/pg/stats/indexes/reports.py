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


class IndexesUsageHints(Report):
    """
    Standard SQL Report
    """

    def __init__(self, pg_conn_params: Dict[str, Any], **kvargs: Any) -> None:
        self._pg_conn_params = pg_conn_params
        self._command_args = kvargs

    @classmethod
    def get_help(cls) -> str:
        return """Indexes: Usage hints \n
        Columns:\n
            - reason: Reason to be listed\n
            - schema: The schema\n
            - table: Table name\n
            - index: Index name\n
            - index_scan_pct: Index scan percentage\n
            - scans_per_write: Percentage scans/write for the index\n
            - index_size: Index size\n
            - table_size: Table size\n
        """

    def get_name(self) -> str:
        return "indexes_usage_hints"

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


class IndexesUsage(Report):
    """
    Standard SQL Report
    """

    def __init__(self, pg_conn_params: Dict[str, Any], **kvargs: Any) -> None:
        self._pg_conn_params = pg_conn_params
        self._command_args = kvargs

    @classmethod
    def get_help(cls) -> str:
        return """Indexes: Usage \n
        Columns:\n
            - idx_scan: Count of index scans\n
            - all_scans: Total scans, idx and sequential\n
            - idx_scan_pct: pct of idx scans\n
            - writes: Index writes\n
            - scans_per_write: Ratio of idx scans and writes. -1 in case of no writes\n
            - idx_size: Index size\n
            - tbl_size: Table size\n
            - idx_type: Index type. One of: BTREE, HASH, GIST, SPGIST, GIN, BRIN, BLOOM\n
        """

    def get_name(self) -> str:
        return "indexes_usage"

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
