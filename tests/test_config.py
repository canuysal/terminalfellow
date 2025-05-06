"""Tests for the configuration module."""

import os
import json
import pytest
from unittest.mock import patch, mock_open, ANY
from terminalfellow.utils.config import (
    ensure_config_dir,
    load_config,
    save_config,
    get_openai_api_key,
    set_openai_api_key,
    get_config_value,
    DEFAULT_CONFIG_DIR,
    DEFAULT_CONFIG_FILE,
)


@patch("os.makedirs")
def test_ensure_config_dir(mock_makedirs):
    """Test that ensure_config_dir creates the directory."""
    ensure_config_dir()
    mock_makedirs.assert_called_once_with(DEFAULT_CONFIG_DIR, exist_ok=True)


@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
def test_load_config_existing(mock_file, mock_exists):
    """Test loading an existing config file."""
    mock_exists.return_value = True
    config = load_config()
    assert config == {"key": "value"}
    mock_file.assert_called_once_with(DEFAULT_CONFIG_FILE, "r")


@patch("os.path.exists")
@patch("terminalfellow.utils.config.save_config")
def test_load_config_nonexistent(mock_save_config, mock_exists):
    """Test loading a nonexistent config file."""
    mock_exists.return_value = False
    config = load_config()
    assert "openai_api_key" in config
    assert "history_file" in config
    mock_save_config.assert_called_once()


@patch("builtins.open", new_callable=mock_open)
def test_save_config(mock_file):
    """Test saving a config file."""
    config = {"key": "value"}
    save_config(config)
    mock_file.assert_called_once_with(DEFAULT_CONFIG_FILE, "w")
    # Since json.dump writes multiple strings, just check that write was called
    assert mock_file().write.called
    # Check that at least key and value are in the calls
    write_calls = [call[0][0] for call in mock_file().write.call_args_list]
    write_data = "".join(write_calls)
    assert '"key"' in write_data
    assert '"value"' in write_data


@patch.dict(os.environ, {"OPENAI_API_KEY": "test_api_key"})
def test_get_openai_api_key_from_env():
    """Test getting the OpenAI API key from environment variable."""
    api_key = get_openai_api_key()
    assert api_key == "test_api_key"


@patch.dict(os.environ, {}, clear=True)
@patch("terminalfellow.utils.config.load_config")
def test_get_openai_api_key_from_config(mock_load_config):
    """Test getting the OpenAI API key from config file."""
    mock_load_config.return_value = {"openai_api_key": "config_api_key"}
    api_key = get_openai_api_key()
    assert api_key == "config_api_key"


@patch("terminalfellow.utils.config.load_config")
@patch("terminalfellow.utils.config.save_config")
def test_set_openai_api_key(mock_save_config, mock_load_config):
    """Test setting the OpenAI API key."""
    mock_load_config.return_value = {"openai_api_key": "old_key"}
    set_openai_api_key("new_key")
    mock_save_config.assert_called_once_with({"openai_api_key": "new_key"})


@patch("terminalfellow.utils.config.load_config")
def test_get_config_value(mock_load_config):
    """Test getting a config value."""
    mock_load_config.return_value = {"key": "value"}

    # Test getting an existing key
    value = get_config_value("key")
    assert value == "value"

    # Test getting a nonexistent key
    value = get_config_value("nonexistent")
    assert value is None

    # Test getting a nonexistent key with default
    value = get_config_value("nonexistent", "default")
    assert value == "default"
