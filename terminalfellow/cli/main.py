"""Command line interface for Terminal Fellow."""

import os
import sys
import time
import typer
from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich import print as rprint
from typing import Optional, List

from terminalfellow import __version__
from terminalfellow.core.generator import CommandGenerator
from terminalfellow.utils.history import HistoryAnalyzer
from terminalfellow.utils.config import (
    get_openai_api_key,
    set_openai_api_key,
    get_config_value,
    save_config,
    load_config,
)

app = typer.Typer(help="Terminal Fellow: Your intelligent terminal assistant.")
console = Console(stderr=True)  # Use stderr for console output to keep stdout clean
generator = CommandGenerator()
history_analyzer = HistoryAnalyzer()


@app.callback()
def callback():
    """Terminal Fellow: Your intelligent terminal assistant."""


@app.command()
def version():
    """Show the version of Terminal Fellow."""
    rprint(f"Terminal Fellow v{__version__}")


@app.command(name="config")
def configure(
    openai_api_key: Optional[str] = typer.Option(
        None, "--openai-api-key", help="Set OpenAI API key"
    ),
    history_file: Optional[str] = typer.Option(
        None, "--history-file", help="Set the path to the history file"
    ),
    use_history: Optional[bool] = typer.Option(
        None, "--use-history", help="Enable or disable command history usage"
    ),
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
):
    """Configure Terminal Fellow settings."""
    if openai_api_key:
        set_openai_api_key(openai_api_key)
        rprint("[bold green]OpenAI API key set successfully[/]")

    if history_file:
        # Expand tilde in path
        history_file = os.path.expanduser(history_file)
        if not os.path.exists(history_file):
            rprint(
                f"[bold yellow]Warning:[/] History file {history_file} does not exist"
            )

        config = load_config()
        config["history_file"] = history_file
        save_config(config)
        rprint(f"[bold green]History file set to:[/] {history_file}")

    if use_history is not None:
        config = load_config()
        config["use_history"] = use_history
        save_config(config)
        if use_history:
            rprint("[bold green]Command history usage enabled[/]")
        else:
            rprint("[bold green]Command history usage disabled[/]")

    if show or (not openai_api_key and not history_file and use_history is None):
        # Show current configuration
        api_key = get_openai_api_key() or "[Not set]"
        # Hide full API key
        if api_key != "[Not set]":
            api_key = f"{api_key[:4]}...{api_key[-4:]}"

        history_file = get_config_value("history_file", "[Not set]")
        use_history = get_config_value("use_history", False)

        rprint("[bold blue]Current Configuration:[/]")
        rprint(f"[bold]OpenAI API Key:[/] {api_key}")
        rprint(f"[bold]History File:[/] {history_file}")
        rprint(f"[bold]Use Command History:[/] {'Yes' if use_history else 'No'}")


def interactive_config():
    """Run interactive configuration if no API keys are found."""
    console.print("\n[bold blue]Welcome to Terminal Fellow![/]")
    console.print("Let's set up your configuration...\n")

    # Ask for OpenAI API key
    api_key = get_openai_api_key()
    if not api_key:
        console.print("[yellow]No OpenAI API key found.[/]")
        api_key = typer.prompt("Enter your OpenAI API key", hide_input=True)
        if not api_key:
            console.print("[bold red]No API key provided. Configuration cancelled.[/]")
            return False

        set_openai_api_key(api_key)
        console.print("[green]API key saved successfully![/]")

    # Ask about history usage
    config = load_config()
    if "use_history" not in config:
        use_history = typer.confirm(
            "Would you like to use command history for context?", default=True
        )
        config["use_history"] = use_history
        save_config(config)

        if use_history:
            # Check if history file path is set and valid
            history_file = config.get("history_file")
            if not history_file or not os.path.exists(os.path.expanduser(history_file)):
                # Try to detect shell type and set default history file
                shell = os.environ.get("SHELL", "")
                if "zsh" in shell:
                    default_history = "~/.zsh_history"
                elif "fish" in shell:
                    default_history = "~/.local/share/fish/fish_history"
                else:
                    default_history = "~/.bash_history"

                history_file = typer.prompt(
                    f"Path to your shell history file", default=default_history
                )

                # Expand the path and save
                history_file = os.path.expanduser(history_file)
                if not os.path.exists(history_file):
                    console.print(
                        f"[yellow]Warning: {history_file} does not exist. Please check the path.[/]"
                    )

                config["history_file"] = history_file
                save_config(config)

    console.print(
        "\n[bold green]Configuration complete![/] You can now use Terminal Fellow.\n"
    )
    return True


def generate_command(prompt):
    """Generate a command based on the natural language prompt."""
    try:
        # Check if API key exists, if not run interactive config
        if not get_openai_api_key():
            config_success = interactive_config()
            # If still no API key, exit
            if not config_success or not get_openai_api_key():
                console.print(
                    "[bold red]No OpenAI API key found. Please run 'tfa config' to set up your configuration.[/]"
                )
                return False

        # Prepare context based on config
        context = {}
        config = load_config()

        # Add current directory to context
        context["cwd"] = os.getcwd()

        # Add history if enabled in config
        if config.get("use_history", False):
            try:
                history_data = history_analyzer.analyze_history()
                if history_data and "most_recent" in history_data:
                    context["history"] = "\n".join(history_data["most_recent"])
            except Exception as e:
                console.print(
                    f"[bold yellow]Warning: Could not analyze history: {str(e)}[/]"
                )

        # Generate the command with spinner
        with console.status("[bold yellow]Generating command...[/]", spinner="dots"):
            try:
                command = generator.generate(prompt, context)
            except Exception as e:
                console.print(f"[bold red]Error generating command: {str(e)}[/]")
                return False

        # Clear the line with carriage return and print the command
        sys.stdout.write("\r\033[K")  # Clear the current line
        print(command)  # Print just the command for easy copy-paste
        return True
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {str(e)}[/]")
        return False


def main():
    """The main entry point for the CLI application."""
    try:
        # Get all command line arguments
        args = sys.argv[1:]

        # Show help if no arguments
        if not args:
            app(["--help"])
            return

        # Handle specific commands
        if args[0] == "config":
            # Extract just the config arguments
            config_args = args[1:] if len(args) > 1 else []
            app(["config"] + config_args)
            return

        if args[0] == "version":
            app(["version"])
            return

        if args[0] in ["--help", "-h", "help"]:
            app(["--help"])
            return

        # If no specific command matched, treat everything as prompt
        prompt = " ".join(args)
        if not prompt.strip():
            console.print("[bold yellow]Please provide a prompt after 'tfa'[/]")
            return

        # Generate command based on prompt
        generate_command(prompt)

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Operation cancelled by user.[/]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {str(e)}[/]")
        sys.exit(1)


if __name__ == "__main__":
    main()
