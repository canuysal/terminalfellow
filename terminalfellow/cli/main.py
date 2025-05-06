"""Command line interface for Terminal Fellow."""

import os
import sys
import time
import typer
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich import print as rprint
from typing import Optional, List
import enum

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


class ModelProvider(str, enum.Enum):
    OPENAI = "OpenAI"
    CLAUDE = "Claude (Coming Soon)"
    GEMINI = "Gemini (Coming Soon)"


class OpenAIModel(str, enum.Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"


@app.callback()
def callback():
    """Terminal Fellow: Your fellow terminal assistant."""


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
    # If --config is provided without other args, run interactive config
    if len(sys.argv) == 2 and sys.argv[1] == "--config":
        interactive_config()
        return

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
        model_provider = get_config_value("model_provider", "OpenAI")
        model = get_config_value("model", "gpt-3.5-turbo")

        rprint("[bold blue]Current Configuration:[/]")
        rprint(f"[bold]Model Provider:[/] {model_provider}")
        rprint(f"[bold]Model:[/] {model}")
        rprint(f"[bold]API Key:[/] {api_key}")
        rprint(f"[bold]History File:[/] {history_file}")
        rprint(f"[bold]Use Command History:[/] {'Yes' if use_history else 'No'}")


def interactive_config():
    """Run interactive configuration wizard for Terminal Fellow."""
    console.print("\n[bold blue]Terminal Fellow Configuration Wizard[/]")
    console.print("[blue]----------------------------------------[/]\n")

    config = load_config()

    # Step 1: Select model provider
    console.print("[bold]Step 1:[/] Select AI Provider")
    provider_options = [provider.value for provider in ModelProvider]

    provider_choice = questionary.select(
        "", choices=provider_options, default=provider_options[0]
    ).ask()

    if provider_choice in [ModelProvider.CLAUDE.value, ModelProvider.GEMINI.value]:
        console.print(
            f"\n[yellow]Note: {provider_choice} is coming soon. Using OpenAI for now.[/]\n"
        )
        provider_choice = ModelProvider.OPENAI.value

    config["model_provider"] = provider_choice
    console.print(f"[green]Selected provider: {provider_choice}[/]\n")

    # Step 2: Select OpenAI model
    console.print("[bold]Step 2:[/] Select OpenAI Model")
    model_options = [model.value for model in OpenAIModel]

    model_choice = questionary.select(
        "", choices=model_options, default=model_options[0]
    ).ask()

    config["model"] = model_choice
    console.print(f"[green]Selected model: {model_choice}[/]\n")

    # Step 3: Set API key
    console.print("[bold]Step 3:[/] Set API Key")
    current_api_key = get_openai_api_key()
    if current_api_key:
        masked_key = f"{current_api_key[:4]}...{current_api_key[-4:]}"
        console.print(f"Current API key: {masked_key}")
        change_key = questionary.confirm(
            "Do you want to change your API key?", default=False
        ).ask()
        if change_key:
            api_key = questionary.password("Enter your OpenAI API key:").ask()
            set_openai_api_key(api_key)
            console.print("[green]API key updated successfully![/]\n")
    else:
        api_key = questionary.password("Enter your OpenAI API key:").ask()
        if not api_key:
            console.print("[bold red]No API key provided. Configuration cancelled.[/]")
            return False
        set_openai_api_key(api_key)
        console.print("[green]API key saved successfully![/]\n")

    # Step 4: Configure history usage
    console.print("[bold]Step 4:[/] Command History")
    use_history = questionary.confirm(
        "Would you like to use command history for context?",
        default=config.get("use_history", True),
    ).ask()

    config["use_history"] = use_history

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

            history_file = questionary.text(
                "Path to your shell history file:", default=default_history
            ).ask()

            # Expand the path and save
            history_file = os.path.expanduser(history_file)
            if not os.path.exists(history_file):
                console.print(
                    f"[yellow]Warning: {history_file} does not exist. Please check the path.[/]"
                )

            config["history_file"] = history_file

    # Save configuration
    save_config(config)

    # Show final configuration
    console.print("\n[bold blue]Configuration Complete![/]")
    console.print("[blue]----------------------[/]")

    console.print("[bold]Your Configuration:[/]")
    console.print(f"  Provider: [green]{config.get('model_provider')}[/]")
    console.print(f"  Model: [green]{config.get('model')}[/]")
    api_key = get_openai_api_key() or "[Not set]"
    if api_key != "[Not set]":
        api_key = f"{api_key[:4]}...{api_key[-4:]}"
    console.print(f"  API Key: [green]{api_key}[/]")
    console.print(
        f"  Use History: [green]{'Yes' if config.get('use_history') else 'No'}[/]"
    )
    if config.get("use_history"):
        console.print(
            f"  History File: [green]{config.get('history_file', '[Not set]')}[/]"
        )

    # Show example usage
    console.print("\n[bold]Example Usage:[/]")
    console.print("  [green]tfa find all pdf files created in the last 7 days[/]")
    console.print("  [green]tfa extract audio from my_video.mp4[/]")
    console.print("  [green]tfa create a backup of my project directory[/]")

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
                    "[bold red]No OpenAI API key found. Please run 'tfa --config' to set up your configuration.[/]"
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
        if args[0] == "--config":
            interactive_config()
            return

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
