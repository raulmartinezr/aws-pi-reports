"""Input validation module"""
from typing import Union

import typer


def validate_ssh_tunnel_inputs(
    ssh_host: Union[str, None] = None,
    ssh_key_path: Union[str, None] = None,
    ssh_user: Union[str, None] = None,
    ssh_pass: Union[str, None] = None,
) -> None:
    """Validate ssh tunnel inputs"""
    if not ssh_host:
        typer.Abort("ssh_host is required when ssh_tunnel is enabled")
    if not ssh_user:
        typer.Abort("ssh_user is required when ssh_tunnel is enabled")
    if not ssh_key_path and not ssh_pass:
        typer.Abort("One of the supported SSH authentication methods is required: key (ssh_key_path) or password ( ssh_pass)")
