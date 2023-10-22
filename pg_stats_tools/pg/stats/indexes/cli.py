"""SQL module"""

from typing import Annotated, Any, Dict

import typer

from pg_stats_tools.format import TableFormatOption
from pg_stats_tools.pg.cli import pg_params
from pg_stats_tools.pg.stats.indexes.reports import IndexesUsage, IndexesUsageHints

indexes = typer.Typer(
    help="""Index based reports
    """
)


@indexes.command(help=IndexesUsageHints.get_help())
def index_usage_hints(
    format: Annotated[
        TableFormatOption,
        typer.Option(help="Output table format", case_sensitive=True),
    ] = TableFormatOption.github,
    schema: Annotated[
        str,
        typer.Option(help="Schema. Default: public. Use _all to get all schemas"),
    ] = "public",
) -> None:
    # frame: Union[FrameType, None] = inspect.currentframe()
    # f_name = frame.f_code.co_name if frame else "unknown_function"
    command_args: Dict[str, Any] = {"format": format.value, "schema": schema}
    IndexesUsageHints(pg_conn_params=pg_params, **command_args).run()


@indexes.command(help=IndexesUsage.get_help())
def index_usage(
    format: Annotated[
        TableFormatOption,
        typer.Option(help="Output table format", case_sensitive=True),
    ] = TableFormatOption.github,
    schema: Annotated[
        str,
        typer.Option(help="Schema. Default: public. Use _all to get all schemas"),
    ] = "public",
) -> None:
    # frame: Union[FrameType, None] = inspect.currentframe()
    # f_name = frame.f_code.co_name if frame else "unknown_function"
    command_args: Dict[str, Any] = {"format": format.value, "schema": schema}
    IndexesUsage(pg_conn_params=pg_params, **command_args).run()
