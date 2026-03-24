![GitHub release](https://img.shields.io/github/v/release/Sneiden/Python-Dictionary-IP-MAC)
![GitHub license](https://img.shields.io/github/license/Sneiden/Python-Dictionary-IP-MAC)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey)
![Nmap](https://img.shields.io/badge/requires-nmap-green)


# Python-Dictionary-IP-MAC

A Python CLI tool that scans a local network using **Nmap** and generates a structured JSON dictionary of all discovered **IP** and **MAC** addresses, including vendor and hostname information.

---

## Requirements

- Python 3.8+
- [Nmap](https://nmap.org/download.html) installed and available in `PATH`
- Windows OS (uses `ipconfig` for network detection)
- **Run as Administrator** (required for MAC address resolution via Nmap)

---

## 📦 Latest Release

[![GitHub release](https://img.shields.io/github/v/release/Sneiden/Python-Dictionary-IP-MAC)](https://github.com/Sneiden/Python-Dictionary-IP-MAC/releases/latest)

Download the latest version from the [Releases page](https://github.com/Sneiden/Python-Dictionary-IP-MAC/releases/latest).

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Sneiden/Python-Dictionary-IP-MAC.git
cd Python-Dictionary-IP-MAC

# 2. Install Nmap
# Download from https://nmap.org/download.html and add to PATH

# 3. No pip dependencies required — uses Python standard library only
```

---

## Usage

```bash
# Run as Administrator (required for MAC address resolution)
cd src
python main.py
```

### Step by step

```
1. The tool detects all active network interfaces via ipconfig
2. You select which interface to scan from a numbered list
3. Nmap scans the network range and discovers active hosts
4. Results are parsed, structured and exported to output/
```

---

## Configuration

All configurable values are managed from `config/settings.json`:

```json
{
    "scan": {
        "nmap_flags": ["-sn", "-PR", "-oX", "-"],
        "timeout_seconds": 60
    },
    "output": {
        "directory": "output",
        "filename_prefix": "Network_Dictionary"
    },
    "logging": {
        "level": "DEBUG",
        "directory": "logs"
    }
}
```

| Setting | Description |
|---|---|
| `nmap_flags` | Flags passed to the Nmap command |
| `timeout_seconds` | Max scan duration in seconds. Set to `null` to wait indefinitely | `null` |
| `output.directory` | Directory where JSON results are saved |
| `filename_prefix` | Prefix for the generated JSON filename |
| `logging.level` | Minimum log level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `logging.directory` | Directory where log files are saved |

---

## Project Structure

```
Python-Dictionary-IP-MAC/
├── src/
│   ├── main.py                  # Entry point — orchestrates the pipeline
│   ├── modules/
│   │   ├── network_info.py      # Detects network range via ipconfig
│   │   ├── scanner.py           # Runs Nmap scan and returns XML output
│   │   ├── parser.py            # Parses and depurates Nmap XML output
│   │   └── exporter.py          # Structures and exports JSON dictionary
│   └── utils/
│       ├── config.py            # Loads and exposes settings.json
│       ├── logger.py            # Centralized file and console logging
│       └── spinner.py           # Animated CLI spinner for blocking tasks
├── config/
│   └── settings.json            # Project configuration
├── tests/
│   └── test_parser.py           # Unit tests for parser module
├── output/                      # Generated JSON files (git-ignored)
├── logs/                        # Daily log files (git-ignored)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Output Format

Results are saved to `output/Network_Dictionary_<timestamp>.json`:

```json
{
    "scan_timestamp": "2026-03-21T10:00:00",
    "total_devices": 3,
    "localhost": {
        "ip": "192.168.1.33",
        "mac": "N/A",
        "vendor": "N/A",
        "hostname": "PC",
        "type": "localhost"
    },
    "remote_devices": [
        {
            "ip": "192.168.1.1",
            "mac": "AA:BB:CC:DD:EE:FF",
            "vendor": "Cisco Systems",
            "hostname": "router.local",
            "type": "remote"
        },
        {
            "ip": "192.168.1.20",
            "mac": "FF:EE:DD:CC:BB:AA",
            "vendor": "Example Vendor",
            "hostname": "Example Hostname",
            "type": "remote"
        }
    ]
}
```

---

## Running Tests

```bash
python -m unittest tests/test_parser.py -v
```

Tests do not require Nmap or Administrator privileges.

---

## Logging

Daily log files are saved to `logs/scan_<date>.log`:

- **Console** → `INFO` level and above
- **Log file** → Configured via `logging.level` in `settings.json`

Log level can be changed at any time in `config/settings.json` without touching code.

---

## Git Branches

| Branch | Purpose |
|---|---|
| `main` | Stable releases only |
| `development` | Default integration branch |
| `feature/*` | New functionality |
| `bugfix/*` | Bug fixes |
| `refactor/*` | Code restructuring |
| `docs/*` | Documentation only |
| `test/*` | Tests only |

---

## Notes

- `ipconfig` is Windows-only — cross-platform support is not in scope
- Nmap `-sn` flag performs host discovery without port scanning
- Nmap `-PR` uses ARP ping for more reliable host discovery on local networks
- Nmap `-oX -` outputs XML directly to stdout for clean pipeline processing
- The localhost device (the machine running the scan) is included in results and tagged with `type: localhost`
- All hardcoded values have been replaced by `config/settings.json` — no code changes needed for common adjustments
