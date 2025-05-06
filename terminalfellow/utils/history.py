"""Shell history analyzer for Terminal Fellow."""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from collections import Counter

from terminalfellow.utils.config import get_config_value


class HistoryAnalyzer:
    """Analyze shell command history."""

    def __init__(self, history_file: Optional[str] = None):
        """Initialize the history analyzer.

        Args:
            history_file: Path to the shell history file. If None, uses the default.
        """
        self.history_file = history_file or self._get_default_history_path()

    def _get_default_history_path(self) -> str:
        """Get the default shell history file path.

        Returns:
            Path to the default shell history file
        """
        # Get history file from config, or default to bash history
        return get_config_value("history_file", os.path.expanduser("~/.bash_history"))

    def read_history(self) -> List[str]:
        """Read the shell history file.

        Returns:
            List of history entries
        """
        if not os.path.exists(self.history_file):
            return []

        with open(self.history_file, "r", encoding="utf-8", errors="ignore") as f:
            return [line.strip() for line in f if line.strip()]

    def analyze_history(self) -> Dict[str, Any]:
        """Analyze the shell history.

        Returns:
            Dictionary with analysis results
        """
        history = self.read_history()
        max_items = get_config_value("max_history_items", 10)

        # Create command frequency counter
        command_counter: Counter = Counter()
        for cmd in history:
            # Use the first word as the command name
            command_name = cmd.split()[0] if cmd and " " in cmd else cmd
            command_counter[command_name] += 1

        # Find most common commands
        common_commands = command_counter.most_common(10)

        return {
            "count": len(history),
            "most_recent": history[-max_items:] if history else [],
            "common_commands": common_commands,
            # More sophisticated analysis to be added
        }
