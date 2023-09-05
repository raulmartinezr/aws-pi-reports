"""cli for RDS reports"""
import inspect
from enum import Enum
from types import FrameType
from typing import Annotated, Any, Dict, Union

import pandas as pd
import typer
from rich import print
from rich.panel import Panel
from rich.pretty import Pretty
from tabulate import tabulate

from aws_pi_reports.aws import AWSClient
from aws_pi_reports.psql import execute_sql
from aws_pi_reports.rds.reports import StandardRDSReport, StandardRDSReportBuilder
from aws_pi_reports.reports import ReportRunner, read_sql_input

sql_params: Dict[str, Any] = {}


app = typer.Typer(
    help="""Performance Reports for RDS
    """
)


api = typer.Typer(
    help="""Performance Insights Reports for RDS
    """
)
sql = typer.Typer(
    help="""Performance SQL Reports for RDS
    """
)
app.add_typer(api, name="api")
app.add_typer(sql, name="sql")


@api.command()
def counter_metrics(
    db_id: Annotated[str, typer.Argument(help="The name/id of the database to analyze")] = "dasnano-iam-play-rds-postgres-iam",
    aws_profile: Annotated[str, typer.Argument(envvar="AWS_PROFILE")] = "play",
    aws_region: Annotated[str, typer.Argument(envvar="AWS_REGION")] = "eu-west-1",
) -> None:
    frame: Union[FrameType, None] = inspect.currentframe()
    f_name = frame.f_code.co_name if frame else "unknown_function"
    report: StandardRDSReport = (
        StandardRDSReportBuilder().with_report_name(f_name).with_client(AWSClient(aws_profile=aws_profile, aws_region=aws_region)).build()
    )
    ReportRunner().run(report=report, db_id=db_id)


@api.command(
    help="""Database load average grouped by TOP wait events \n
            Dimension: db.load.avg -> The number of active sessions for the DB engine measured as average number of active sessions.
    """
)
def load_avg_top_wait_events(
    db_id: Annotated[str, typer.Argument(help="The name/id of the database to analyze")] = "dasnano-iam-play-rds-postgres-iam",
    aws_profile: Annotated[str, typer.Argument(envvar="AWS_PROFILE")] = "play",
    aws_region: Annotated[str, typer.Argument(envvar="AWS_REGION")] = "eu-west-1",
) -> None:
    frame: Union[FrameType, None] = inspect.currentframe()
    f_name = frame.f_code.co_name if frame else "unknown_function"
    report: StandardRDSReport = (
        StandardRDSReportBuilder().with_report_name(f_name).with_client(AWSClient(aws_profile=aws_profile, aws_region=aws_region)).build()
    )
    ReportRunner().run(report=report, db_id=db_id)


@app.command(
    help="""Database load average grouped by TOP SQL statements \n
            Dimension: db.load.avg -> The number of active sessions for the DB engine measured as average number of active sessions.
    """
)
def load_avg_top_sql(
    db_id: Annotated[str, typer.Argument(help="The name/id of the database to analyze")] = "dasnano-iam-play-rds-postgres-iam",
    aws_profile: Annotated[str, typer.Argument(envvar="AWS_PROFILE")] = "play",
    aws_region: Annotated[str, typer.Argument(envvar="AWS_REGION")] = "eu-west-1",
) -> None:
    frame: Union[FrameType, None] = inspect.currentframe()
    f_name = frame.f_code.co_name if frame else "unknown_function"
    report: StandardRDSReport = (
        StandardRDSReportBuilder().with_report_name(f_name).with_client(AWSClient(aws_profile=aws_profile, aws_region=aws_region)).build()
    )
    ReportRunner().run(report=report, db_id=db_id)


class SQLAvgTimeSqlTypeOrderByField(str, Enum):
    avg_time_ms = "avg_time_ms"
    num_calls = "num_calls"
    total_time_ms = "total_time_ms"
    max_time_ms = "max_time_ms"


class TableFormatOption(str, Enum):
    plain = "plain"
    simple = "simple"
    github = "github"
    grid = "grid"
    simple_grid = "simple_grid"
    rounded_grid = "rounded_grid"
    heavy_grid = "heavy_grid"
    mixed_grid = "mixed_grid"
    double_grid = "double_grid"
    fancy_grid = "fancy_grid"
    outline = "outline"
    simple_outline = "simple_outline"
    rounded_outline = "rounded_outline"
    heavy_outline = "heavy_outline"
    mixed_outline = "mixed_outline"
    double_outline = "double_outline"
    fancy_outline = "fancy_outline"
    pipe = "pipe"
    orgtbl = "orgtbl"
    asciidoc = "asciidoc"
    jira = "jira"
    presto = "presto"
    pretty = "pretty"
    psql = "psql"
    rst = "rst"
    mediawiki = "mediawiki"
    moinmoin = "moinmoin"
    youtrack = "youtrack"
    html = "html"
    unsafehtml = "unsafehtml"
    latex = "latex"
    latex_raw = "latex_raw"
    latex_booktabs = "latex_booktabs"
    latex_longtable = "latex_longtable"
    textile = "textile"
    tsv = "tsv"


@sql.callback()
def sql_callback(
    ssh_user: Annotated[str, typer.Option(help="SSH user", envvar="SSH_USER")] = "",
    db_user: Annotated[str, typer.Option(help="Database user", envvar="DB_USER")] = "",
    db_name: Annotated[str, typer.Option(help="Database used to connect to", envvar="DB_NAME")] = "",
    db_host: Annotated[str, typer.Option(help="Database user password", envvar="DB_HOST")] = "",
    db_port: Annotated[int, typer.Option(help="Database user password", envvar="DB_PORT")] = 5432,
    ssh_tunnel: Annotated[bool, typer.Option(help="Whether to use SSH tunneling to connect to database or not", envvar="SSH_TUNNEL")] = False,
    ssh_host: Annotated[str, typer.Option(help="SSH host", envvar="SSH_HOST")] = "",
    ssh_port: Annotated[int, typer.Option(help="Whether to use SSH tunneling to connect to database or not", envvar="SSH_PORT")] = 5432,
    ssh_key_path: Annotated[str, typer.Option(help="Path to the key to connect via SSH", envvar="SSSH_KEY_PATH")] = "",
    ssh_key_pass: Annotated[str, typer.Option(help="Password for SSH key file", envvar="SSSH_KEY_PASS")] = "",
    ssh_pass: Annotated[str, typer.Option(help="SSH user password", envvar="SSH_PASS")] = "",
    db_pass: Annotated[str, typer.Option(help="Database user password", envvar="DB_PASS")] = "",
) -> None:
    sql_params["ssh_user"] = ssh_user
    sql_params["db_user"] = db_user
    sql_params["db_name"] = db_name
    sql_params["db_host"] = db_host
    sql_params["db_port"] = db_port
    sql_params["ssh_tunnel"] = ssh_tunnel
    sql_params["ssh_host"] = ssh_host
    sql_params["ssh_port"] = ssh_port
    sql_params["ssh_key_path"] = ssh_key_path
    sql_params["ssh_key_pass"] = ssh_key_pass
    sql_params["ssh_pass"] = ssh_pass
    sql_params["db_pass"] = db_pass


sql_avg_time_sqltype_help = """Average response time for SQL statements by SQL type \n
        Fields:\n
            - sql_type: The type of SQL statement\n
            - avg_time_ms: The average amount of time each SQL statement type took to run, in milliseconds\n
            - num_calls: The number of times each SQL statement type was called\n
            - total_time_ms: The total amount of time each SQL statement type took to run, in milliseconds\n
            - max_time_ms: The maximum amount of time each SQL statement  type took to run, in millisecondsq\n

"""


@sql.command(help=sql_avg_time_sqltype_help)
def sql_avg_time_sqltype(
    order_by: Annotated[
        SQLAvgTimeSqlTypeOrderByField,
        typer.Option(help="Field used to specify the order in which the result set should be sorted", case_sensitive=True),
    ] = SQLAvgTimeSqlTypeOrderByField.avg_time_ms,
    format: Annotated[
        TableFormatOption,
        typer.Option(help="Output table format", case_sensitive=True),
    ] = TableFormatOption.psql,
) -> None:
    frame: Union[FrameType, None] = inspect.currentframe()
    f_name = frame.f_code.co_name if frame else "unknown_function"

    command_args: Dict[str, Any] = {
        "order_by": order_by.value,
        "format": format.value,
    }
    sql: str = read_sql_input(f_name, **command_args)
    df: pd.DataFrame = execute_sql(
        sql=sql,
        **sql_params,
    )

    help_panel = Panel(sql_avg_time_sqltype_help, title="Help", height=sql_avg_time_sqltype_help.count("\n"))
    input_panel = Panel(Pretty(command_args), title="Input", height=len(command_args) + 3)

    # layout["Info"]["input"].size=200
    print(help_panel)
    print(input_panel)
    print(tabulate(df, headers="keys", tablefmt=format.value))  # pyright: ignore
