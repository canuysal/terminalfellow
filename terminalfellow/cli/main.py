"""Command line interface for Terminal Fellow."""

import os
import typer
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint
from typing import Optional, List

from terminalfellow import __version__
from terminalfellow.core.generator import CommandGenerator
from terminalfellow.utils.history import HistoryAnalyzer
from terminalfellow.utils.config import get_openai_api_key, set_openai_api_key, get_config_value

app = typer.Typer()
console = Console()
generator = CommandGenerator()
history_analyzer = HistoryAnalyzer()

@app.callback()
def callback():
    """Terminal Fellow: Your intelligent terminal assistant."""

@app.command()
def version():
    """Show the version of Terminal Fellow."""
    rprint(f"Terminal Fellow v{__version__}")

@app.command(name="generate")
def generate_command(
    query: str = typer.Argument(..., help="Natural language command request"),
    use_history: bool = typer.Option(False, "--history", "-h", help="Use command history for context"),
    execute: bool = typer.Option(False, "--execute", "-e", help="Execute the generated command"),
    advanced: bool = typer.Option(False, "--advanced", "-a", help="Use advanced prompt for command generation")
):
    """Generate a command based on natural language request."""
    rprint(f"[bold green]Query:[/] {query}")

    # Prepare context based on options
    context = {}

    if use_history:
        # Get command history
        history_data = history_analyzer.analyze_history()
        if history_data and "most_recent" in history_data:
            context["history"] = "\n".join(history_data["most_recent"])
            rprint("[yellow]Using command history for context[/]")

    # Use current directory as context
    context["cwd"] = os.getcwd()

    # Use advanced prompt if requested
    prompt_type = "advanced" if advanced else "default"
    custom_generator = CommandGenerator(config={"prompt_type": prompt_type})

    rprint("[yellow]Generating command...[/]")

    # Generate the command with context
    command = custom_generator.generate(query, context)

    # Display the generated command
    panel = Panel(
        command,
        title="[bold blue]Generated Command[/]",
        border_style="blue",
        padding=(1, 2)
    )
    console.print(panel)

    # Execute the command if requested
    if execute:
        rprint("[yellow]Executing command...[/]")
        try:
            os.system(command)
        except Exception as e:
            rprint(f"[bold red]Error executing command:[/] {e}")

@app.command(name="alias", help="Create an alias for the tfa command")
def create_alias(shell: str = typer.Option("bash", help="Shell type (bash, zsh)")):
    """Create an alias for the Terminal Fellow Assistant."""
    if shell == "bash":
        rprint("""
[bold green]Add the following to your ~/.bashrc file:[/]

alias tfa='python -m terminalfellow.cli.main generate'
        """)
    elif shell == "zsh":
        rprint("""
[bold green]Add the following to your ~/.zshrc file:[/]

alias tfa='python -m terminalfellow.cli.main generate'
        """)
    else:
        rprint(f"[bold red]Unsupported shell:[/] {shell}")

@app.command(name="config")
def configure(
    openai_api_key: Optional[str] = typer.Option(None, "--openai-api-key", help="Set OpenAI API key"),
    history_file: Optional[str] = typer.Option(None, "--history-file", help="Set the path to the history file"),
    show: bool = typer.Option(False, "--show", help="Show current configuration")
):
    """Configure Terminal Fellow settings."""
    if openai_api_key:
        set_openai_api_key(openai_api_key)
        rprint("[bold green]OpenAI API key set successfully[/]")

    if history_file:
        # Expand tilde in path
        history_file = os.path.expanduser(history_file)
        if not os.path.exists(history_file):
            rprint(f"[bold yellow]Warning:[/] History file {history_file} does not exist")

        from terminalfellow.utils.config import save_config, load_config
        config = load_config()
        config["history_file"] = history_file
        save_config(config)
        rprint(f"[bold green]History file set to:[/] {history_file}")

    if show or (not openai_api_key and not history_file):
        # Show current configuration
        api_key = get_openai_api_key() or "[Not set]"
        # Hide full API key
        if api_key != "[Not set]":
            api_key = f"{api_key[:4]}...{api_key[-4:]}"

        history_file = get_config_value("history_file", "[Not set]")

        rprint("[bold blue]Current Configuration:[/]")
        rprint(f"[bold]OpenAI API Key:[/] {api_key}")
        rprint(f"[bold]History File:[/] {history_file}")

if __name__ == "__main__":
    app()