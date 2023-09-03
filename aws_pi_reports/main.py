"""Main entry for typer CLI"""
import typer

from aws_pi_reports.rds import cli as rds

app: typer.Typer = typer.Typer(
    help="""Welcome to AWS Pertformance Insights Reports cli tool
    """
)

app.add_typer(rds.app, name="rds")
# app.add_typer(docdb.app, name="docdb")

if __name__ == "__main__":
    app()
