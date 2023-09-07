"""cli for RDS reports"""

from typing import Annotated, Any, Dict

import typer

pg_params: Dict[str, Any] = {}


pg = typer.Typer(
    help="""Performance Reports for Postgres
    """
)


@pg.callback()
def sql_callback(
    ssh_user: Annotated[str, typer.Option(help="SSH user", envvar="SSH_USER")] = "",
    db_user: Annotated[str, typer.Option(help="Database user", envvar="DB_USER")] = "",
    db_name: Annotated[str, typer.Option(help="Database used to connect to", envvar="DB_NAME")] = "",
    db_host: Annotated[str, typer.Option(help="Database user password", envvar="DB_HOST")] = "",
    db_port: Annotated[int, typer.Option(help="Database user password", envvar="DB_PORT")] = 5432,
    ssh_tunnel: Annotated[
        bool,
        typer.Option(help="Whether to use SSH tunneling to connect to database or not", envvar="SSH_TUNNEL"),
    ] = False,
    ssh_host: Annotated[str, typer.Option(help="SSH host", envvar="SSH_HOST")] = "",
    ssh_port: Annotated[
        int,
        typer.Option(help="Whether to use SSH tunneling to connect to database or not", envvar="SSH_PORT"),
    ] = 5432,
    ssh_key_path: Annotated[str, typer.Option(help="Path to the key to connect via SSH", envvar="SSSH_KEY_PATH")] = "",
    ssh_key_pass: Annotated[str, typer.Option(help="Password for SSH key file", envvar="SSSH_KEY_PASS")] = "",
    ssh_pass: Annotated[str, typer.Option(help="SSH user password", envvar="SSH_PASS")] = "",
    db_pass: Annotated[str, typer.Option(help="Database user password", envvar="DB_PASS")] = "",
) -> None:
    pg_params["ssh_user"] = ssh_user
    pg_params["db_user"] = db_user
    pg_params["db_name"] = db_name
    pg_params["db_host"] = db_host
    pg_params["db_port"] = db_port
    pg_params["ssh_tunnel"] = ssh_tunnel
    pg_params["ssh_host"] = ssh_host
    pg_params["ssh_port"] = ssh_port
    pg_params["ssh_key_path"] = ssh_key_path
    pg_params["ssh_key_pass"] = ssh_key_pass
    pg_params["ssh_pass"] = ssh_pass
    pg_params["db_pass"] = db_pass


# api = typer.Typer(
#     help="""Performance Insights Reports for RDS
#     """
# )


# app.add_typer(api, name="api")


# @api.command()
# def counter_metrics(
#     db_id: Annotated[str, typer.Argument(help="The name/id of the database to analyze")] = "dasnano-iam-play-rds-postgres-iam",
#     aws_profile: Annotated[str, typer.Argument(envvar="AWS_PROFILE")] = "play",
#     aws_region: Annotated[str, typer.Argument(envvar="AWS_REGION")] = "eu-west-1",
# ) -> None:
#     frame: Union[FrameType, None] = inspect.currentframe()
#     f_name = frame.f_code.co_name if frame else "unknown_function"
#     report: StandardRDSReport = (
#         StandardRDSReportBuilder().with_report_name(f_name).with_client(AWSClient(aws_profile=aws_profile, aws_region=aws_region)).build()
#     )
#     ReportRunner().run(report=report, db_id=db_id)


# @api.command(
#     help="""Database load average grouped by TOP wait events \n
#             Dimension: db.load.avg -> The number of active sessions for the DB engine measured as average number of active sessions.
#     """
# )
# def load_avg_top_wait_events(
#     db_id: Annotated[str, typer.Argument(help="The name/id of the database to analyze")] = "dasnano-iam-play-rds-postgres-iam",
#     aws_profile: Annotated[str, typer.Argument(envvar="AWS_PROFILE")] = "play",
#     aws_region: Annotated[str, typer.Argument(envvar="AWS_REGION")] = "eu-west-1",
# ) -> None:
#     frame: Union[FrameType, None] = inspect.currentframe()
#     f_name = frame.f_code.co_name if frame else "unknown_function"
#     report: StandardRDSReport = (
#         StandardRDSReportBuilder().with_report_name(f_name).with_client(AWSClient(aws_profile=aws_profile, aws_region=aws_region)).build()
#     )
#     ReportRunner().run(report=report, db_id=db_id)


# @app.command(
#     help="""Database load average grouped by TOP SQL statements \n
#             Dimension: db.load.avg -> The number of active sessions for the DB engine measured as average number of active sessions.
#     """
# )
# def load_avg_top_sql(
#     db_id: Annotated[str, typer.Argument(help="The name/id of the database to analyze")] = "dasnano-iam-play-rds-postgres-iam",
#     aws_profile: Annotated[str, typer.Argument(envvar="AWS_PROFILE")] = "play",
#     aws_region: Annotated[str, typer.Argument(envvar="AWS_REGION")] = "eu-west-1",
# ) -> None:
#     frame: Union[FrameType, None] = inspect.currentframe()
#     f_name = frame.f_code.co_name if frame else "unknown_function"
#     report: StandardRDSReport = (
#         StandardRDSReportBuilder().with_report_name(f_name).with_client(AWSClient(aws_profile=aws_profile, aws_region=aws_region)).build()
#     )
#     ReportRunner().run(report=report, db_id=db_id)
