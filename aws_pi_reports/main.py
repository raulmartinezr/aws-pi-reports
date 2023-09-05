"""Main entry for typer CLI"""
import typer
from dotenv import load_dotenv

from aws_pi_reports.rds import cli as rds

load_dotenv()
# print(os.environ)

app: typer.Typer = typer.Typer(
    help="""Welcome to AWS Pertformance Insights Reports cli tool
    """,
    rich_markup_mode="rich",
)


app.add_typer(rds.app, name="rds")
# app.add_typer(docdb.app, name="docdb")

if __name__ == "__main__":
    app()
