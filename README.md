# Terminal Fellow

A CLI tool that understands your command line history and generates commands or scripts based on natural language requests.

## Features

- Parse natural language requests to generate relevant terminal commands
- Analyze user's command history to understand context and preferences
- Generate one-liners or scripts based on the request and historical usage patterns
- Understand and reference project structures and common workflows

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/terminalfellow.git
cd terminalfellow

# Set up a virtual environment (recommended)
conda create -n terminalfellow python=3.12
conda activate terminalfellow

# Install the package
pip install -e .
```

## Configuration

Terminal Fellow can be configured to use the OpenAI API for more intelligent command generation:

```bash
# Set your OpenAI API key
python -m terminalfellow.cli.main config --openai-api-key "your-api-key"

# Set a custom shell history file (default is ~/.bash_history)
python -m terminalfellow.cli.main config --history-file ~/.zsh_history

# Show current configuration
python -m terminalfellow.cli.main config --show
```

## Usage

```bash
# Basic usage - generate a command
python -m terminalfellow.cli.main generate "list all Python files in the current directory"

# Use command history as context
python -m terminalfellow.cli.main generate "repeat the last git command" --history

# Use advanced mode for more precise commands
python -m terminalfellow.cli.main generate "find all files modified in the last 24 hours" --advanced

# Generate and execute the command
python -m terminalfellow.cli.main generate "create a backup of this directory" --execute

# Create an alias for easier usage
python -m terminalfellow.cli.main alias

# Or add to your ~/.bashrc:
# alias tfa='python -m terminalfellow.cli.main generate'
```

### Using the CLI

After installation, you can use the `tfa` command directly:

```bash
# Basic usage
tfa generate "list files modified today"

# With options
tfa generate "find large files" --advanced --execute

# Configure
tfa config --openai-api-key "your-api-key"
```

### Command Line Options

- `--history`, `-h`: Use command history for context
- `--advanced`, `-a`: Use advanced prompt for command generation
- `--execute`, `-e`: Execute the generated command

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Or install individually
pip install pytest black flake8 mypy pre-commit types-setuptools

# Run tests
pytest
```

## License

See the [LICENSE](LICENSE) file for details.