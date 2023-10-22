"""SQL module"""

from typing import Annotated, Any, Dict

import typer

from pg_stats_tools.format import TableFormatOption
from pg_stats_tools.pg.cli import pg_params
from pg_stats_tools.pg.stats.buffers.reports import TableCacheHits, IndexCacheHits, Usage

buffers = typer.Typer(
    help="""Buffer based reports
    """
)


@buffers.command(help=TableCacheHits.get_help())
def table_cache_hits(
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
    TableCacheHits(pg_conn_params=pg_params, **command_args).run()


@buffers.command(help=IndexCacheHits.get_help())
def index_cache_hits(
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
    IndexCacheHits(pg_conn_params=pg_params, **command_args).run()


@buffers.command(help=Usage.get_help())
def usage(
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
    Usage(pg_conn_params=pg_params, **command_args).run()
