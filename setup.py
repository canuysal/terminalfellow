from setuptools import setup, find_packages

setup(
    name="terminalfellow",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "llama-index",
        "chromadb",
        "pydantic",
        "typer",
        "rich",
        "questionary",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.2",
            "black>=23.9.1",
            "flake8>=6.1.0",
            "mypy>=1.5.1",
            "pytest-mock>=3.11.1",
            "types-setuptools>=80.3.0.20250505",
            "pre_commit>=4.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tf=terminalfellow.cli.main:main",
        ],
    },
    author="Can Uysal",
    description=(
        "CLI tool that understands command line history and "
        "generates commands based on natural language"
    ),
    python_requires=">=3.8",
)
