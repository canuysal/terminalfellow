"""Command line interface for Terminal Fellow."""

import typer
from rich.console import Console
from rich import print as rprint

from terminalfellow import __version__
from terminalfellow.core.generator import CommandGenerator

app = typer.Typer()
console = Console()
generator = CommandGenerator()

@app.callback()
def callback():
    """Terminal Fellow: Your intelligent terminal assistant."""

@app.command()
def version():
    """Show the version of Terminal Fellow."""
    rprint(f"Terminal Fellow v{__version__}")

@app.command()
def generate(query: str = typer.Argument(..., help="Natural language command request")):
    """Generate a command based on natural language request."""
    rprint(f"[bold green]Query:[/] {query}")
    rprint("[yellow]Generating command...[/]")

    # Use the command generator to generate a command
    command = generator.generate(query)

    rprint(f"[bold blue]Generated command:[/] {command}")

if __name__ == "__main__":
    app()