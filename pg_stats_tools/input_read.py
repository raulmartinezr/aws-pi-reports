"""Reports module"""
from __future__ import annotations

import json
import os
from typing import Any

from jinja2 import Template
from rich.console import Console

console = Console()


def read_report_input(report_name: str) -> Any:
    json_file_path = os.path.join(os.path.dirname(__file__), "reports_inputs", f"{report_name}.json")
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def read_sql_input(report_name: str, **kvargs: Any) -> str:
    json_file_path = os.path.join(os.path.dirname(__file__), "reports_inputs", f"{report_name}.sql")
    with open(json_file_path, "r") as file:
        data = file.read()
    return Template(data).render(**kvargs)





# class ReportRunner:
#     def __init__(self) -> None:
#         super().__init__()

#     def run(self, report: Report, db_id: str) -> None:
#         print("[bold green]Starting report[/bold green]")
#         report_input = report.read_report_input()
#         print("[blue]Input[/blue] read")
#         report_input_processed = report.processs_report_input(report_input=report_input)
#         print("[blue]Report input[/blue] processed read")
#         query_output = report.query(query_input=report_input_processed, db_id=db_id)
#         print("[blue]Performance Insights[/blue] data queried")
#         print("[blue]Response[/blue]:")
#         console.print_json(json=json.dumps(query_output, indent=4, sort_keys=True, default=str))
#         report_input_processed = report.report(report_input=query_output)
#         print("[blue]Report generated [/blue] [bold green]successfully[/bold green]")
