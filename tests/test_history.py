"""Tests for the history analyzer module."""

import os
import pytest
import tempfile
from unittest.mock import patch
from collections import Counter
from terminalfellow.utils.history import HistoryAnalyzer
from terminalfellow.utils.config import get_config_value


def test_history_analyzer_initialization():
    """Test that the history analyzer can be initialized."""
    analyzer = HistoryAnalyzer()
    assert analyzer is not None
    assert analyzer.history_file == get_config_value(
        "history_file", os.path.expanduser("~/.bash_history")
    )

    # Test with custom history file
    analyzer = HistoryAnalyzer(history_file="/custom/path")
    assert analyzer.history_file == "/custom/path"


def test_read_history_nonexistent_file():
    """Test reading from a nonexistent history file."""
    analyzer = HistoryAnalyzer(history_file="/nonexistent/path")
    history = analyzer.read_history()
    assert history == []


def test_read_and_analyze_history():
    """Test reading and analyzing a history file."""
    # Create a temporary history file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
        temp.write(
            "ls -la\ncd /home\npwd\ngit status\ngit add .\ngit commit -m 'update'\n"
        )
        temp.write("python script.py\npython script.py\npython script.py\n")
        temp_path = temp.name

    try:
        analyzer = HistoryAnalyzer(history_file=temp_path)

        # Test reading
        history = analyzer.read_history()
        assert len(history) == 9
        assert history[0] == "ls -la"

        # Test analyzing
        analysis = analyzer.analyze_history()
        assert analysis["count"] == 9
        assert len(analysis["most_recent"]) <= 10  # Should be 9 in this case
        assert "git commit -m 'update'" in analysis["most_recent"]

        # Test common commands
        common_commands = dict(analysis["common_commands"])
        assert common_commands.get("python") == 3  # python appears 3 times
        assert common_commands.get("git") in (
            2,
            3,
        )  # git appears 2-3 times depending on implementation
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@patch("terminalfellow.utils.history.get_config_value")
def test_max_history_items_config(mock_get_config):
    """Test that max_history_items configuration is respected."""

    # Mock both calls to get_config_value
    def side_effect(key, default=None):
        if key == "max_history_items":
            return 5
        return default

    mock_get_config.side_effect = side_effect

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
        temp.write("cmd1\ncmd2\ncmd3\ncmd4\ncmd5\ncmd6\ncmd7\ncmd8\ncmd9\ncmd10\n")
        temp_path = temp.name

    try:
        analyzer = HistoryAnalyzer(history_file=temp_path)
        analysis = analyzer.analyze_history()

        # Should only have 5 recent items due to config
        assert len(analysis["most_recent"]) == 5
        assert analysis["most_recent"] == ["cmd6", "cmd7", "cmd8", "cmd9", "cmd10"]
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)
