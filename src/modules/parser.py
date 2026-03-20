import xml.etree.ElementTree as ET
from typing import List, Dict


def parse_nmap_output(raw_xml: str) -> List[Dict[str, str]]:
    """
    Parses raw Nmap XML output and returns a structured list of devices.

    Each device dictionary contains:
        - ip (str): IPv4 address
        - mac (str): MAC address or 'N/A' if not found
        - vendor (str): NIC vendor or 'N/A' if not found
        - hostname (str): Resolved hostname or 'N/A' if not found

    Args:
        raw_xml (str): Raw XML string returned by the Nmap scan.

    Returns:
        List[Dict[str, str]]: List of discovered devices.

    Raises:
        ValueError: If the XML input is empty or malformed.
    """
    pass