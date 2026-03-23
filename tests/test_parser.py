import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from modules.parser import parse_nmap_output

import logging
logging.disable(logging.CRITICAL)

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

    def test_ip_extraction(self):
        """Each device should have a valid IPv4 address."""
        ips = [device["ip"] for device in self.devices]
        self.assertIn("192.168.1.33", ips)
        self.assertIn("192.168.1.1", ips)
        self.assertIn("192.168.1.20", ips)
    
    def test_mac_extraction(self):
        """Remote devices should have their MAC address extracted correctly."""
        router = next(d for d in self.devices if d["ip"] == "192.168.1.1")
        self.assertEqual(router["mac"], "AA:BB:CC:DD:EE:FF")

    def test_vendor_extraction(self):
        """Remote devices should have their vendor extracted correctly."""
        router = next(d for d in self.devices if d["ip"] == "192.168.1.1")
        self.assertEqual(router["vendor"], "Cisco Systems")

    def test_hostname_extraction(self):
        """Devices should have their hostname extracted correctly."""
        router = next(d for d in self.devices if d["ip"] == "192.168.1.1")
        self.assertEqual(router["hostname"], "router.local")

    def test_hostname_localhost(self):
        """Localhost device should have its hostname extracted correctly."""
        localhost = next(d for d in self.devices if d["type"] == "localhost")
        self.assertEqual(localhost["hostname"], "Admin")
    
    def test_localhost_tagged(self):
        """Device with reason='localhost-response' should be tagged as localhost."""
        localhost = next(d for d in self.devices if d["ip"] == "192.168.1.33")
        self.assertEqual(localhost["type"], "localhost")

    def test_localhost_no_mac(self):
        """Localhost device should have no MAC address."""
        localhost = next(d for d in self.devices if d["type"] == "localhost")
        self.assertEqual(localhost["mac"], "N/A")

    def test_remote_tagged(self):
        """Devices with reason='arp-response' should be tagged as remote."""
        remote_devices = [d for d in self.devices if d["type"] == "remote"]
        self.assertEqual(len(remote_devices), 2)

    def test_remote_has_mac(self):
        """Remote devices should have a valid MAC address."""
        remote_devices = [d for d in self.devices if d["type"] == "remote"]
        for device in remote_devices:
            self.assertNotEqual(device["mac"], "N/A")

    def test_host_with_no_ip_filtered(self):
        """Hosts with no valid IP address should be filtered out."""
        ips = [device["ip"] for device in self.devices]
        self.assertNotIn("N/A", ips)

    def test_total_after_depuration(self):
        """Sample XML has 4 hosts but 1 has no IP — only 3 should remain."""
        self.assertEqual(len(self.devices), 3)

    def test_empty_input_raises_value_error(self):
        """Empty XML input should raise a ValueError."""
        with self.assertRaises(ValueError):
            parse_nmap_output("")

    def test_whitespace_input_raises_value_error(self):
        """Whitespace-only XML input should raise a ValueError."""
        with self.assertRaises(ValueError):
            parse_nmap_output("   ")

if __name__ == "__main__":
    unittest.main()