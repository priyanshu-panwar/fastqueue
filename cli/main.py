import typer

from cli.queue import queue_cli
from cli.auth import app as auth_app

cli = typer.Typer(help="FastQueue CLI for managing queues")
cli.add_typer(queue_cli, name="queue")
cli.add_typer(auth_app, name="auth")

if __name__ == "__main__":
    cli()
