"""Configuration utilities for Terminal Fellow."""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Default configuration directory
DEFAULT_CONFIG_DIR = os.path.expanduser("~/.config/terminalfellow")
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_DIR, "config.json")

def ensure_config_dir() -> None:
    """Ensure the configuration directory exists."""
    os.makedirs(DEFAULT_CONFIG_DIR, exist_ok=True)

def load_config() -> Dict[str, Any]:
    """Load configuration from the config file.

    Returns:
        The loaded configuration as a dictionary
    """
    ensure_config_dir()

    if not os.path.exists(DEFAULT_CONFIG_FILE):
        # Create a default configuration file
        default_config = {
            "openai_api_key": "",
            "history_file": os.path.expanduser("~/.bash_history"),
            "default_prompt_type": "default",
            "max_history_items": 10,
        }
        save_config(default_config)
        return default_config

    try:
        with open(DEFAULT_CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # Return a default configuration if the file can't be loaded
        return {
            "openai_api_key": "",
            "history_file": os.path.expanduser("~/.bash_history"),
            "default_prompt_type": "default",
            "max_history_items": 10,
        }

def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to the config file.

    Args:
        config: The configuration to save
    """
    ensure_config_dir()

    with open(DEFAULT_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_openai_api_key() -> Optional[str]:
    """Get the OpenAI API key from environment variable or config file.

    Returns:
        The OpenAI API key, or None if not found
    """
    # First try environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key

    # Then try config file
    config = load_config()
    return config.get("openai_api_key")

def set_openai_api_key(api_key: str) -> None:
    """Set the OpenAI API key in the config file.

    Args:
        api_key: The OpenAI API key to set
    """
    config = load_config()
    config["openai_api_key"] = api_key
    save_config(config)

def get_config_value(key: str, default: Any = None) -> Any:
    """Get a configuration value by key.

    Args:
        key: The configuration key to retrieve
        default: The default value to return if the key is not found

    Returns:
        The configuration value for the key, or the default value
    """
    config = load_config()
    return config.get(key, default)