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
    pass