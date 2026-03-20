import json
import os
from datetime import datetime
from typing import List, Dict


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
    output_dir = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "output"
        )
    os.makedirs(output_dir, exist_ok=True)

if __name__ == "__main__":
    import os
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {os.path.abspath(output_dir)}")
    print(f"Exists: {os.path.exists(output_dir)}")