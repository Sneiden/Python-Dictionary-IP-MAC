import subprocess
from utils.logger import setup_logger

logger = setup_logger()

def get_network_range() -> str:

    """
    Detects the local network range to be scanned.

    Runs 'ipconfig' to extract the local IP address and subnet mask,
    then converts them to CIDR notation (e.g., 192.168.1.0/24).
    Raises:
        RuntimeError: If IP or subnet mask cannot be detected.
    Returns:
        str: Network range in CIDR notation.
    """

    result = subprocess.run(
        ["ipconfig"],
        capture_output=True,
        text=True
    )
    output = result.stdout
    logger.debug("Raw ipconfig output captured.")

    interfaces = []
    current_name = None
    current_ip = None
    current_subnet = None

    for line in output.splitlines():
        # Detect interface name (e.g. "Ethernet adapter Ethernet:")
        if line.strip() == "" or line.startswith(" "):
            pass
        elif line.endswith(":"):
            current_name = line.strip().rstrip(":")
            current_ip = None
            current_subnet = None

        if "IPv4 Address" in line:
            current_ip = line.split(":")[-1].strip()
        if "Subnet Mask" in line:
            current_subnet = line.split(":")[-1].strip()

        if current_name and current_ip and current_subnet:
            interfaces.append({
                "name": current_name,
                "ip": current_ip,
                "subnet": current_subnet
            })
            current_name = None
            current_ip = None
            current_subnet = None

    if not interfaces:
        logger.error("No active network interfaces found.")
        raise RuntimeError("No active network interfaces found.")

    if len(interfaces) == 1:
        iface = interfaces[0]
        logger.info(f"One interface found: {iface['name']} — {iface['ip']}")
        print(f"\nOne interface found: {iface['name']} — {iface['ip']}")
        confirm = input("Use this interface? [y/n]: ").strip().lower()
        if confirm != "y":
            logger.warning("Scan cancelled by user during interface selection.")
            raise RuntimeError("Scan cancelled by user.")
        selected = iface
    else:
        print("\nAvailable network interfaces:")
        for i, iface in enumerate(interfaces):
            print(f"  [{i + 1}] {iface['name']} — {iface['ip']}")
        logger.debug(f"Found {len(interfaces)} interfaces, prompting user to select.")
        print()
        while True:
            choice = input(f"Select an interface [1-{len(interfaces)}]: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(interfaces):
                selected = interfaces[int(choice) - 1]
                break
            print(f"  Invalid choice. Please enter a number between 1 and {len(interfaces)}.")

    try:
        network_range = _to_cidr(selected["ip"], selected["subnet"])
    except Exception:
        logger.error(f"Failed to calculate CIDR for '{selected['name']}'. IP: {selected['ip']}, Subnet: {selected['subnet']}")
        raise RuntimeError(
            f"Could not calculate network range for '{selected['name']}'. "
            f"IP: {selected['ip']}, Subnet: {selected['subnet']}"
        )
    logger.info(f"Selected interface: {selected['name']} — {network_range}")
    print(f"\n  Selected: {selected['name']} — {network_range}\n")
    return network_range

def _to_cidr(ip: str, subnet: str) -> str:
    """
    Converts an IP address and subnet mask to CIDR notation.

    Args:
        ip (str): Local IP address (e.g., '192.168.1.100').
        subnet (str): Subnet mask (e.g., '255.255.255.0').

    Returns:
        str: CIDR notation (e.g., '192.168.1.0/24').
    """
    mask_bits = sum(bin(int(x)).count("1") for x in subnet.split("."))
    network_base = ".".join(
        str(int(a) & int(b))
        for a, b in zip(ip.split("."), subnet.split("."))
    )
    return f"{network_base}/{mask_bits}"

