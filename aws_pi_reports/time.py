import re
from datetime import datetime, timedelta
from typing import Dict, Tuple, Union

duration_regex_str = "^((?P<weeks>[-+\\d]+?)w|(?P<days>[-+\\d]+?)d|(?P<hours>[-+\\d]+?)h|(?P<minutes>[-+\\d]+?)m)$"
duration_regex = re.compile(r"{}".format(duration_regex_str))


def parse_time(time: datetime, duration: str) -> Tuple[datetime, datetime]:
    parts: Union[re.Match[str], None] = duration_regex.match(duration)
    if not parts:
        raise SyntaxError(f"Invalid duration string: {duration}. Expected format: {duration_regex_str}")
    groups = parts.groupdict()
    filtered_groups = {k: v for k, v in groups.items() if v is not None}
    time_params: Dict[str, int] = {}
    name = next(iter(filtered_groups))
    value: int = int(filtered_groups[name])
    time_params[name] = abs(value)
    return (time, time + timedelta(**time_params)) if value > 0 else (time - timedelta(**time_params), time)
