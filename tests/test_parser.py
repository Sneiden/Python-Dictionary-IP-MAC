import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from modules.parser import parse_nmap_output


SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<nmaprun>
    <host>
        <status state="up" reason="localhost-response" reason_ttl="0" />
        <address addr="192.168.1.33" addrtype="ipv4" />
        <hostnames>
            <hostname name="Admin" type="PTR" />
        </hostnames>
    </host>
    <host>
        <status state="up" reason="arp-response" reason_ttl="0" />
        <address addr="192.168.1.1" addrtype="ipv4" />
        <address addr="AA:BB:CC:DD:EE:FF" addrtype="mac" vendor="Cisco Systems" />
        <hostnames>
            <hostname name="router.local" type="PTR" />
        </hostnames>
    </host>
    <host>
        <status state="up" reason="arp-response" reason_ttl="0" />
        <address addr="192.168.1.20" addrtype="ipv4" />
        <address addr="FF:EE:DD:CC:BB:AA" addrtype="mac" vendor="Test vendor" />
        <hostnames>
            <hostname name="Test name" type="PTR" />
        </hostnames>
    </host>
    <host>
        <status state="up" reason="arp-response" reason_ttl="0" />
        <hostnames>
        </hostnames>
    </host>
</nmaprun>"""


class TestParser(unittest.TestCase):
    def setUp(self):
        self.devices = parse_nmap_output(SAMPLE_XML)

    def test_device_count(self):
        """Total devices should be 3 — the host with no IP is filtered out."""
        self.assertEqual(len(self.devices), 3)


if __name__ == "__main__":
    unittest.main()