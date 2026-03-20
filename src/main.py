from modules.network_info import get_network_range

def main():
    # Step 1: Get network range
    network_range = get_network_range()
    print(network_range)

if __name__ == "__main__":
    main()