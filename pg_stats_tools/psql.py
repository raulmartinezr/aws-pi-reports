"""postgres sql exection module"""
from typing import Union

import pandas as pd
import psycopg2
import sshtunnel


def execute_sql(
    sql: str,
    db_user: str,
    db_name: str,
    db_pass: str,
    db_host: str,
    ssh_tunnel: bool = False,
    ssh_host: Union[str, None] = None,
    ssh_port: int = 22,
    ssh_key_path: Union[str, None] = None,
    ssh_key_pass: Union[str, None] = None,
    ssh_user: Union[str, None] = None,
    ssh_pass: Union[str, None] = None,
    db_port: int = 5432,
) -> pd.DataFrame:
    data: pd.DataFrame
    if ssh_tunnel:
        with sshtunnel.open_tunnel(  # pyright: ignore[reportUnknownMemberType]
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_pkey=ssh_key_path,
            ssh_private_key_password=None if ssh_key_pass in [None, ""] else ssh_key_pass,
            ssh_password=None if ssh_pass in [None, ""] else ssh_pass,
            remote_bind_address=(db_host, db_port),
            # local_bind_address=("0.0.0.0", 10022),
            # debug_level=1,
        ) as tunnel:
            # tunnel.start()
            local_port: int = int(tunnel.local_bind_port)  # pyright: ignore

            with psycopg2.connect(host="127.0.0.1", port=local_port, database=db_name, user=db_user, password=db_pass) as conn:
                data = pd.read_sql_query(sql, conn)  # pyright: ignore[reportUnknownMemberType]
            return data
    else:
        with psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_pass) as conn:
            data = pd.read_sql_query(sql, conn)  # pyright: ignore[reportUnknownMemberType]
        return data
