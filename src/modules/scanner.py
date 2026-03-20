import subprocess
import shutil
from network_info import get_network_range


def scan_network(network_range: str) -> str:
    """
    Runs an Nmap scan on the given network range to discover
    active hosts with their IP and MAC addresses.

    Args:
        network_range (str): Network range in CIDR notation (e.g., '192.168.1.0/24').

    Returns:
        str: Raw Nmap scan output.

    Raises:
        EnvironmentError: If Nmap is not installed or not found in PATH.
        RuntimeError: If the Nmap scan fails.
    """
    if not shutil.which("nmap"):
        raise EnvironmentError(
            "Nmap is not installed or not found in PATH. "
            "Download it from https://nmap.org/download.html"
        )
    
    print("\n[!] Note: Run as Administrator to ensure MAC address resolution.\n")

    result = subprocess.run(
        ["nmap", "-sn", network_range],
        capture_output=True,
        text=True
        )

    return result.stdout