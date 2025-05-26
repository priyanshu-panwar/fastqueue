import typer

from cli.queue import queue_cli

cli = typer.Typer(help="FastQueue CLI for managing queues")
cli.add_typer(queue_cli, name="queue")

if __name__ == "__main__":
    cli()
