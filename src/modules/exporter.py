import json
import os
from datetime import datetime
from typing import List, Dict
from utils.config import get_config, _get_project_root
from utils.logger import setup_logger

logger = setup_logger()

def export_to_json(devices: List[Dict[str, str]]) -> str:
    """
    Structures the device list into a dictionary and exports
    it as a JSON file in the output/ directory.

    Args:
        devices (List[Dict[str, str]]): List of parsed device dictionaries.

    Returns:
        str: Absolute path of the generated JSON file.

    Raises:
        OSError: If the output directory cannot be created or the file cannot be written.
    """
    config = get_config()

    output_dir = os.path.join(
        _get_project_root(),
        config["output_directory"]
    )
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        logger.error(f"Failed to create output directory '{output_dir}': {e}")
        raise OSError(f"Failed to create output directory '{output_dir}': {e}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{config['filename_prefix']}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    logger.debug(f"Output file path resolved: {os.path.abspath(filepath)}")

    payload = {
        "scan_timestamp": datetime.now().isoformat(),
        "total_devices": len(devices),
        "localhost": next((d for d in devices if d["type"] == "localhost"), None),
        "remote_devices": [d for d in devices if d["type"] == "remote"]
    }
    logger.debug(f"Payload structured: {len(payload['remote_devices'])} remote devices, localhost: {payload['localhost'] is not None}")

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4, ensure_ascii=False)
    except OSError as e:
        logger.error(f"Failed to write network dictionary to '{filepath}': {e}")
        raise OSError(
            f"Failed to write network dictionary to '{filepath}': {e}"
        )

    logger.info(f"Network dictionary exported to: {os.path.abspath(filepath)}")
    return os.path.abspath(filepath)
