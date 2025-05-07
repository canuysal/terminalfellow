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

On first use, Terminal Fellow will walk you through the configuration process with the command:

```bash
# Run the interactive configuration wizard
tf --config
```

The wizard allows you to:
- Select AI provider (currently supports OpenAI with Claude and Gemini coming soon)
- Choose the OpenAI model (gpt-3.5-turbo, gpt-4, gpt-4-turbo)
- Set or update your API key
- Configure command history usage (wip)



## Usage

After installation, simply use the `tf` command followed by your request:

```bash
# Basic usage
tf convert all pdfs in this directory to markdown and move it to a new folder "markdown_converted"

# The entire text after "tf" is treated as your request
tf tf extract audio from my_video.mp4

# You can use it in a pipeline
tf create a JSON file with my CPU info
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