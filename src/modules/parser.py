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
    if not raw_xml or not raw_xml.strip():
        raise ValueError("Nmap output is empty.")

    try:
        root = ET.fromstring(raw_xml)
    except ET.ParseError as e:
        raise ValueError(f"Failed to parse Nmap XML output: {e}")

    hosts = root.findall("host")
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

        devices.append(device)

    devices = [
        device for device in devices
        if device["ip"] != "N/A"
    ]

    return devices

if __name__ == "__main__":
    from network_info import get_network_range
    from scanner import scan_network
    network_range = get_network_range()
    raw_xml = scan_network(network_range)
    devices = parse_nmap_output(raw_xml)
    for device in devices:
        print(device)