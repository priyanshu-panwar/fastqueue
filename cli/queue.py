import typer
from rich.table import Table
from rich.console import Console

from app.core.queue.registry import QueueRegistry
from app.core.queue.schemas import Queue as QueueSchema
from app.core.queue.service import (
    create_queue as create_queue_service,
    delete_queue as delete_queue_service,
    get_all_queues as list_queues_service,
    get_queue_by_name,
)
from app.database import get_db

queue_cli = typer.Typer(help="Queue management commands")
console = Console()


@queue_cli.command("create")
def create_queue():
    """
    Create a new queue.
    """
    name = typer.prompt("Enter queue name", type=str)

    if QueueRegistry.exists(name):
        typer.secho(f"Queue '{name}' already exists.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    queue = QueueSchema(name=name)
    db = next(get_db())
    try:
        create_queue_service(db, queue)
    except Exception as e:
        typer.secho(f"Error creating queue: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    finally:
        db.close()

    typer.secho(f"✅ Queue '{name}' created successfully.", fg=typer.colors.GREEN)


@queue_cli.command("list")
def list_queues():
    """
    List all queues.
    """
    db = next(get_db())
    queues = list_queues_service(db)
    db.close()

    if not queues:
        typer.secho("No queues found.", fg=typer.colors.YELLOW)
        return

    table = Table(title="Queues")
    table.add_column("Name", style="cyan")

    for qm in queues:
        table.add_row(qm.name)

    console.print(table)


@queue_cli.command("delete")
def delete_queue():
    """
    Delete a queue by name.
    """
    name = typer.prompt("Enter queue name to delete", type=str)

    db = next(get_db())
    queue = get_queue_by_name(db, name)
    db.close()
    if not queue:
        typer.secho(f"Queue '{name}' not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    delete_queue_service(db, name)
    typer.secho(f"🗑️ Queue '{name}' deleted.", fg=typer.colors.GREEN)


@queue_cli.command("show")
def show_queue():
    """
    Show details of a queue.
    """
    name = typer.prompt("Enter queue name", type=str)

    db = next(get_db())
    queue = get_queue_by_name(db, name)
    db.close()
    if not queue:
        typer.secho(f"Queue '{name}' not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    console.print(f"[bold cyan]Queue:[/bold cyan] {queue.name}")
    console.print(
        f"[bold magenta]Visibility Timeout:[/bold magenta] {queue.visibility_timeout_seconds} seconds"
    )
