from modules.network_info import get_network_range
from modules.scanner import scan_network
from modules.parser import parse_nmap_output
from modules.exporter import export_to_json
from utils.spinner import Spinner

def main():
    try:
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

        # Step 4: Export to JSON
        filepath = export_to_json(devices)
        print(f"[✓] Network dictionary saved to: {filepath}")

    except EnvironmentError as e:
        print(f"\n[✗] Environment error: {e}")
    except RuntimeError as e:
        print(f"\n[✗] Runtime error: {e}")
    except ValueError as e:
        print(f"\n[✗] Parsing error: {e}")
    except OSError as e:
        print(f"\n[✗] File system error: {e}")
    except KeyboardInterrupt:
        print("\n\n[✗] Scan cancelled by user.")

if __name__ == "__main__":
    main()