"""Tests for the history analyzer module."""
import os
import pytest
import tempfile
from terminalfellow.utils.history import HistoryAnalyzer

def test_history_analyzer_initialization():
    """Test that the history analyzer can be initialized."""
    analyzer = HistoryAnalyzer()
    assert analyzer is not None
    assert analyzer.history_file == os.path.expanduser("~/.bash_history")

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
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
        temp.write("ls -la\ncd /home\npwd\ngit status\n")
        temp_path = temp.name

    try:
        analyzer = HistoryAnalyzer(history_file=temp_path)

        # Test reading
        history = analyzer.read_history()
        assert len(history) == 4
        assert history[0] == "ls -la"

        # Test analyzing
        analysis = analyzer.analyze_history()
        assert analysis["count"] == 4
        assert len(analysis["most_recent"]) == 4
        assert "git status" in analysis["most_recent"]
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)