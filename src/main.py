from modules.network_info import get_network_range
from modules.scanner import scan_network
from modules.parser import parse_nmap_output
from modules.exporter import export_to_json
from utils.spinner import Spinner

def main():
    # Step 1: Get network range
    network_range = get_network_range()
    print(network_range)

if __name__ == "__main__":
    main()