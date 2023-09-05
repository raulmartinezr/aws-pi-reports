"""Reports module"""
from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod
from typing import Any, Literal

from jinja2 import Template
from rich import print
from rich.console import Console

console = Console()


def read_report_input(report_name: str) -> Any:
    json_file_path = os.path.join(os.path.dirname(__file__), "reports_inputs", f"{report_name}.json")
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def read_sql_input(report_name: str, **kvargs: Any) -> Any:
    json_file_path = os.path.join(os.path.dirname(__file__), "reports_inputs", f"{report_name}.sql")
    with open(json_file_path, "r") as file:
        data = file.read()
    return Template(data).render(**kvargs)


class Report(ABC):
    """
    Base Report interface with methods to be implemented by concrete reports
    """

    # @property
    # @abstractmethod
    # def product(self) -> None:
    #     pass

    @abstractmethod
    def get_service_type(self) -> Literal["DOCDB", "RDS"]:
        pass

    @abstractmethod
    def read_report_input(self) -> Any:
        pass

    @abstractmethod
    def processs_report_input(self, report_input: Any) -> Any:
        pass

    @abstractmethod
    def processs_query_output(self, query_output: Any) -> Any:
        pass

    @abstractmethod
    def query(self, query_input: Any, db_id: str) -> Any:
        pass

    @abstractmethod
    def report(self, report_input: Any) -> Any:
        pass


class ReportRunner:
    def __init__(self) -> None:
        super().__init__()

    def run(self, report: Report, db_id: str) -> None:
        print("[bold green]Starting report[/bold green]")
        report_input = report.read_report_input()
        print("[blue]Input[/blue] read")
        report_input_processed = report.processs_report_input(report_input=report_input)
        print("[blue]Report input[/blue] processed read")
        query_output = report.query(query_input=report_input_processed, db_id=db_id)
        print("[blue]Performance Insights[/blue] data queried")
        print("[blue]Response[/blue]:")
        console.print_json(json=json.dumps(query_output, indent=4, sort_keys=True, default=str))
        report_input_processed = report.report(report_input=query_output)
        print("[blue]Report generated [/blue] [bold green]successfully[/bold green]")
