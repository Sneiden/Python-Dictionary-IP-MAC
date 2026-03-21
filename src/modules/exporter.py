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

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Network_Dictionary_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    payload = {
        "scan_timestamp": datetime.now().isoformat(),
        "total_devices": len(devices),
        "localhost": next((d for d in devices if d["type"] == "localhost"), None),
        "remote_devices": [d for d in devices if d["type"] == "remote"]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4, ensure_ascii=False)

    print(f"\n[✓] Network dictionary exported to: {os.path.abspath(filepath)}")
    return os.path.abspath(filepath)


if __name__ == "__main__":
    sample_devices = [
        {"ip": "192.168.1.66", "mac": "N/A", "vendor": "N/A", "hostname": "Admin", "type": "localhost"},
        {"ip": "192.168.1.1", "mac": "AA:BB:CC:DD:EE:FF", "vendor": "Cisco Systems", "hostname": "router.local", "type": "remote"},
        {"ip": "192.168.1.75", "mac": "A8:54:B2:4C:5A:08", "vendor": "Heimgard Technologies", "hostname": "7962v1", "type": "remote"}
    ]
    result = export_to_json(sample_devices)
    print(f"File created at: {result}")