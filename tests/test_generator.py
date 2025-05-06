"""Tests for the command generator module."""
import pytest
from terminalfellow.core.generator import CommandGenerator
from terminalfellow.core import prompts

def test_generator_initialization():
    """Test that the generator can be initialized."""
    generator = CommandGenerator()
    assert generator is not None
    assert generator.config == {}

    # Test with custom config
    generator = CommandGenerator(config={"model": "test-model"})
    assert generator.config == {"model": "test-model"}

def test_generator_generate():
    """Test that the generator can generate commands."""
    generator = CommandGenerator()
    query = "list files in current directory"
    command = generator.generate(query)

    # Check that the command is a string
    assert isinstance(command, str)
    assert command  # Check that it's not empty

    # Advanced query test
    query = "find all python files in the project"
    command = generator.generate(query)
    assert isinstance(command, str)
    assert "find" in command or "python" in command

def test_generator_with_context():
    """Test that the generator can use context information."""
    generator = CommandGenerator()
    query = "go to my project directory"
    context = {
        "cwd": "/home/user",
        "recent_commands": ["cd /home/user/projects/myproject", "git status"]
    }
    command = generator.generate(query, context)

    # Check that it returns a sensible command
    assert isinstance(command, str)
    assert command  # Check that it's not empty

def test_prompt_templates():
    """Test that prompt templates are properly formatted."""
    # Test system prompt retrieval
    system_prompt = prompts.get_system_prompt()
    assert isinstance(system_prompt, str)
    assert "CLI assistant" in system_prompt

    # Test command prompt formatting
    command_prompt = prompts.format_command_prompt(
        prompt_type="default",
        query="list files"
    )
    assert isinstance(command_prompt, str)
    assert "list files" in command_prompt

    # Test with history context
    history_prompt = prompts.format_command_prompt(
        prompt_type="with_history",
        query="repeat last git command",
        history="git status\ngit commit -m 'update'"
    )
    assert isinstance(history_prompt, str)
    assert "repeat last git command" in history_prompt
    assert "git commit" in history_prompt