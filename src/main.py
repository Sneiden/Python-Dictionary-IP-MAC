from modules.network_info import get_network_range
from modules.scanner import scan_network
from modules.parser import parse_nmap_output
from modules.exporter import export_to_json
from utils.spinner import Spinner

def main():
    # Step 1: Get network range
    network_range = get_network_range()

    # Step 2: Run Nmap scan
    spinner = Spinner("Scanning network, this may take a few seconds...")
    spinner.start()
    raw_xml = scan_network(network_range)
    spinner.stop()
    print("[✓] Scan complete.")

    # Step 3: Parse Nmap output
    devices = parse_nmap_output(raw_xml)
    print(f"[✓] Found {len(devices)} devices on the network.")

if __name__ == "__main__":
    main()