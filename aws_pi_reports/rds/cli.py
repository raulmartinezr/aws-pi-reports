"""cli for RDS reports"""
import inspect
from types import FrameType
from typing import Union

import typer

app = typer.Typer(
    help="""Performance Insights Reports for RDS
    """
)


@app.command()
def counter_metrics() -> None:
    frame: Union[FrameType, None] = inspect.currentframe()
    f_name = frame.f_code.co_name if frame else "unknown_function"
    print(f"Executing {f_name}")
