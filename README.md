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

On first use, Terminal Fellow will walk you through the configuration process if no API keys are found.

You can also configure it manually:

```bash
# Configure Terminal Fellow
tfa config

# Set your OpenAI API key
tfa config --openai-api-key "your-api-key"

# Set a custom shell history file (default is ~/.bash_history)
tfa config --history-file ~/.zsh_history

# Enable or disable command history usage
tfa config --use-history true

# Show current configuration
tfa config --show
```

## Usage

After installation, simply use the `tfa` command followed by your request:

```bash
# Basic usage
tfa list files modified today

# The entire text after "tfa" is treated as your request
tfa find all python files and count their lines

# You can use it in a pipeline
tfa create a JSON file with my CPU info | jq
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Or install individually
pip install pytest pre-commit

# Run tests
pytest
```

### Code Style and Linting

The project uses the following tools for code quality:

- **Black**: Code formatting (line length: 88)
- **MyPy**: Static type checking
- **Pre-commit**: Automated checks before commits

To set up pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install
```

## License

See the [LICENSE](LICENSE) file for details.