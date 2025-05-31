import typer
from app.database import get_db
from app.auth2 import service

app = typer.Typer(help="User management CLI")


@app.command("create")
def create_user():
    """
    Create a new user with username and password.
    """
    username = typer.prompt("Enter username")
    password = typer.prompt("Enter password", hide_input=True, confirmation_prompt=True)

    db = next(get_db())
    try:
        user = service.create_user(db, username, password)
        typer.echo(f"✅ User '{user.username}' created successfully.")
    finally:
        db.close()


@app.command("delete")
def delete_user():
    """
    Delete a user by username and password.
    """
    username = typer.prompt("Enter username")
    password = typer.prompt("Enter password", hide_input=True)

    db = next(get_db())
    try:
        result = service.delete_user(db, username, password)
        typer.echo(f"🗑️ User '{username}' deleted.")
    finally:
        db.close()


@app.command("change-password")
def change_password():
    """
    Change password for a given user.
    """
    username = typer.prompt("Enter username")
    old_password = typer.prompt("Enter old password", hide_input=True)
    new_password = typer.prompt(
        "Enter new password", hide_input=True, confirmation_prompt=True
    )

    db = next(get_db())
    try:
        user = service.change_password(db, username, old_password, new_password)
        typer.echo(f"🔐 Password updated for user '{user.username}'.")
    finally:
        db.close()
