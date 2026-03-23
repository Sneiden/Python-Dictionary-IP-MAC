import subprocess
import shutil
from utils.logger import setup_logger

logger = setup_logger()

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
        logger.error("Nmap is not installed or not found in PATH.")
        raise EnvironmentError(
            "Nmap is not installed or not found in PATH. "
            "Download it from https://nmap.org/download.html"
        )
    
    print("\n[!] Note: Run as Administrator to ensure MAC address resolution.\n")
    logger.debug(f"Starting Nmap scan on network range: {network_range}")

    result = subprocess.run(
        ["nmap", "-sn", "-PR", network_range, "-oX", "-"],
        capture_output=True,
        text=True
        )

    if result.returncode != 0:
        logger.error(f"Nmap scan failed:\n{result.stderr}")
        raise RuntimeError(
            f"Nmap scan failed with the following error:\n{result.stderr}"
        )

    logger.debug("Nmap scan raw XML output captured successfully.")
    return result.stdout