import subprocess

def get_network_range() -> str:
    """
    Detects the local network range to be scanned.

    Runs 'ipconfig' to extract the local IP address and subnet mask,
    then converts them to CIDR notation (e.g., 192.168.1.0/24).
    Raises:
        RuntimeError: If IP or subnet mask cannot be detected.
    """

    result = subprocess.run(
        ["ipconfig"],
        capture_output=True,
        text=True
    )
    output = result.stdout

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

        print(current_name, current_ip, current_subnet)
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
        raise RuntimeError("No active network interfaces found.")

    if len(interfaces) == 1:
        iface = interfaces[0]
        print(f"\nOne interface found: {iface['name']} — {iface['ip']}")
        confirm = input("Use this interface? [y/n]: ").strip().lower()
        if confirm != "y":
            raise RuntimeError("Scan cancelled by user.")
        selected = iface
    else:
        print("\nAvailable network interfaces:")
        for i, iface in enumerate(interfaces):
            print(f"  [{i + 1}] {iface['name']} — {iface['ip']}")

        print()
        while True:
            choice = input(f"Select an interface [1-{len(interfaces)}]: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(interfaces):
                selected = interfaces[int(choice) - 1]
                break
            print(f"  Invalid choice. Please enter a number between 1 and {len(interfaces)}.")

    return selected

    """
    Returns:
        str: Network range in CIDR notation.
    """


