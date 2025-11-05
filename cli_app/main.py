"""CLI application using Typer."""
import typer
from rich.console import Console
from rich.table import Table

from core.application.use_cases.create_item_uc import CreateItemUseCase
from core.infrastructure.repositories.in_memory_item_repo import InMemoryItemRepository

app = typer.Typer()
console = Console()

repository = InMemoryItemRepository()


@app.command()
def create(
    name: str = typer.Argument(..., help="Name of the item"),
    description: str = typer.Option(
        None, "--description", "-d", help="Description of the item"
    ),
) -> None:
    """Create a new item."""
    use_case = CreateItemUseCase(repository)
    item = use_case.execute(name=name, description=description)

    console.print("✅ Item created successfully!", style="bold green")
    console.print(f"ID: {item.id}")
    console.print(f"Name: {item.name}")
    if item.description:
        console.print(f"Description: {item.description}")


@app.command()
def list() -> None:
    """List all items."""
    items = repository.find_all()

    if not items:
        console.print("No items found.", style="yellow")
        return

    table = Table(title="Items")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Description", style="green")

    for item in items:
        table.add_row(
            str(item.id),
            item.name,
            item.description or ""
        )

    console.print(table)


if __name__ == "__main__":
    app()
