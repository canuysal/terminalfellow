"""Shell history analyzer for Terminal Fellow."""
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

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
        # Default to bash history for now
        return os.path.expanduser("~/.bash_history")

    def read_history(self) -> List[str]:
        """Read the shell history file.

        Returns:
            List of history entries
        """
        if not os.path.exists(self.history_file):
            return []

        with open(self.history_file, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]

    def analyze_history(self) -> Dict[str, Any]:
        """Analyze the shell history.

        Returns:
            Dictionary with analysis results
        """
        history = self.read_history()

        # Simple analysis for now
        return {
            "count": len(history),
            "most_recent": history[-10:] if history else [],
            # More sophisticated analysis to be added
        }