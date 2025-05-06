"""Tests for the command generator module."""
import pytest
from terminalfellow.core.generator import CommandGenerator

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

    # For now, just check that the command contains the query
    assert isinstance(command, str)
    assert query in command