from modules.network_info import get_network_range
from modules.scanner import scan_network
from modules.parser import parse_nmap_output
from modules.exporter import export_to_json
from utils.spinner import Spinner
from utils.logger import setup_logger

logger = setup_logger()


def main():
    try:
        logger.info("Starting IP/MAC network scan...")

        # Step 1: Get network range
        network_range = get_network_range()
        logger.info(f"Network range detected: {network_range}")

        # Step 2: Run Nmap scan
        spinner = Spinner("Scanning network, this may take a few seconds...")
        spinner.start()
        raw_xml = scan_network(network_range)
        spinner.stop()
        print("[✓] Scan complete.")
        logger.info("Nmap scan completed successfully.")

        # Step 3: Parse Nmap output
        devices = parse_nmap_output(raw_xml)
        print(f"[✓] Found {len(devices)} devices on the network.")
        logger.info(f"Parsed {len(devices)} devices from scan output.")

        # Step 4: Export to JSON
        filepath = export_to_json(devices)
        print(f"[✓] Network dictionary saved to: {filepath}")
        logger.info(f"Network dictionary exported to: {filepath}")

    except EnvironmentError as e:
        logger.error(f"Environment error: {e}")
        print(f"\n[✗] Environment error: {e}")
    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        print(f"\n[✗] Runtime error: {e}")
    except ValueError as e:
        logger.error(f"Parsing error: {e}")
        print(f"\n[✗] Parsing error: {e}")
    except OSError as e:
        logger.error(f"File system error: {e}")
        print(f"\n[✗] File system error: {e}")
    except KeyboardInterrupt:
        logger.warning("Scan cancelled by user.")
        print("\n\n[✗] Scan cancelled by user.")

    input("\nPress Enter to exit...")
        
if __name__ == "__main__":
    main()