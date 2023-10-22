"""Time functions"""

from datetime import datetime

import typer


def parse_timestamp(tstmp: str) -> datetime:
    try:
        return datetime.fromisoformat(tstmp)
    except ValueError:
        raise typer.BadParameter("Invalid timestamp format. Please use ISO format (e.g., 'YYYY-MM-DDTHH:MM:SS')")
