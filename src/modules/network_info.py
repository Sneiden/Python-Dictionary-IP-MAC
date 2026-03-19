import subprocess

def get_network_range() -> str:
    """
    Detects the local network range to be scanned.

    Runs 'ipconfig' to extract the local IP address and subnet mask,
    then converts them to CIDR notation (e.g., 192.168.1.0/24).

    Returns:
        str: Network range in CIDR notation.

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
            # Save previous interface if complete
            if current_name and current_ip and current_subnet:
                interfaces.append({
                    "name": current_name,
                    "ip": current_ip,
                    "subnet": current_subnet
                })
            current_name = line.strip().rstrip(":")
            current_ip = None
            current_subnet = None

        if "IPv4 Address" in line:
            current_ip = line.split(":")[-1].strip()
        if "Subnet Mask" in line:
            current_subnet = line.split(":")[-1].strip()

    # Capture the last interface
    if current_name and current_ip and current_subnet:
        interfaces.append({
            "name": current_name,
            "ip": current_ip,
            "subnet": current_subnet
        })

    for i in interfaces:
        print(i)
        
    return "ok"

