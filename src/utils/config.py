import json
import os
from typing import Any, Dict


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
        os.path.dirname(__file__),
        "..",
        "..",
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
        "timeout_seconds": int(config["scan"]["timeout_seconds"]),
        "output_directory": config["output"]["directory"],
        "filename_prefix": config["output"]["filename_prefix"],
        "log_level": config["logging"]["level"],
        "log_directory": config["logging"]["directory"]
    }