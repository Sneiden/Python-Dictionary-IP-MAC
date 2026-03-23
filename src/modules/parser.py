import xml.etree.ElementTree as ET
from typing import List, Dict
from utils.logger import setup_logger

logger = setup_logger()

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
    if not raw_xml or not raw_xml.strip():
        logger.error("Nmap output is empty.")
        raise ValueError("Nmap output is empty.")

    try:
        root = ET.fromstring(raw_xml)
    except ET.ParseError as e:
        logger.error(f"Failed to parse Nmap XML output: {e}")
        raise ValueError(f"Failed to parse Nmap XML output: {e}")

    hosts = root.findall("host")
    logger.debug(f"Found {len(hosts)} host elements in XML output.")
    devices = []

    for host in hosts:
        device = {
            "ip": "N/A",
            "mac": "N/A",
            "vendor": "N/A",
            "hostname": "N/A",
            "type": "remote"
        }

        # Tag localhost device
        status = host.find("status")
        if status is not None and status.get("reason") == "localhost-response":
            device["type"] = "localhost"
            logger.debug("Localhost device detected and tagged.")

        for address in host.findall("address"):
            addr_type = address.get("addrtype")
            if addr_type == "ipv4":
                device["ip"] = address.get("addr", "N/A")
            elif addr_type == "mac":
                device["mac"] = address.get("addr", "N/A")
                device["vendor"] = address.get("vendor", "N/A")

        hostnames = host.find("hostnames")
        if hostnames is not None:
            first_hostname = hostnames.find("hostname")
            if first_hostname is not None:
                device["hostname"] = first_hostname.get("name", "N/A")

        logger.debug(f"Parsed device: {device['ip']} | {device['mac']} | {device['type']}")
        devices.append(device)

    devices = [
        device for device in devices
        if device["ip"] != "N/A"
    ]

    logger.info(f"Depurated device list: {len(devices)} valid devices.")
    return devices