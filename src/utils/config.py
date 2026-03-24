import sys
import json
import os
from typing import Any, Dict

def _get_project_root() -> str:
    """
    Resolves the project root path correctly both when running
    as a Python script and as a PyInstaller executable.
    """
    if getattr(sys, "frozen", False):
        # Running as PyInstaller executable
        # sys.executable = path to the .exe file
        return os.path.dirname(sys.executable)
    else:
        # Running as a normal Python script
        return os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

def load_config() -> Dict[str, Any]:
    """
    Loads and returns the project configuration from config/settings.json.

    Resolves the config file path relative to the project root,
    parses the JSON content and returns it as a dictionary.

    Returns:
        Dict[str, Any]: Project configuration dictionary.

    Raises:
        FileNotFoundError: If settings.json cannot be found.
        ValueError: If settings.json contains invalid JSON.
    """
    config_path = os.path.join(
        _get_project_root(),
        "config",
        "settings.json"
    )
    config_path = os.path.abspath(config_path)

    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Settings file not found at: {config_path}"
        )

    with open(config_path, "r", encoding="utf-8") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"settings.json contains invalid JSON: {e}"
            )

    return config

def get_config() -> Dict[str, Any]:
    """
    Returns the full configuration dictionary with typed sections.

    Returns:
        Dict[str, Any]: Dictionary with keys:
            - nmap_flags (list): Nmap command flags
            - timeout_seconds (int): Scan timeout in seconds
            - output_directory (str): Output directory path
            - filename_prefix (str): JSON filename prefix
            - log_level (str): Logging level
            - log_directory (str): Log directory path
    """
    config = load_config()

    return {
        "nmap_flags": config["scan"]["nmap_flags"],
        "timeout_seconds": int(config["scan"]["timeout_seconds"]) if config["scan"]["timeout_seconds"] is not None else None,
        "output_directory": config["output"]["directory"],
        "filename_prefix": config["output"]["filename_prefix"],
        "log_level": config["logging"]["level"],
        "log_directory": config["logging"]["directory"]
    }