# Terminal Fellow

A CLI fellow who generates bash commands or scripts based on natural language requests.

It can also understand you better if you let it learn your bash history by using a local vector db.

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

# Currently on dev, so setup a virtual env.
conda create -n terminalfellow
conda activate terminalfellow

# Install the package
pip install -e .
```

## Usage (intended, wip)

```bash
# Basic usage
tfa "go to my last project and start the web server"

# Get help
tfa --help
```

## Current usage:

```
cd terminalfellow/cli
python ./main.py
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

See the [LICENSE](LICENSE) file for details, MIT.