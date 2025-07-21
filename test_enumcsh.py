#!/usr/bin/env python3
"""
Test script for enumCSh.
"""

import os
import json
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the main module
import enumcsh

class TestEnumCSh(unittest.TestCase):
    """Test cases for enumCSh."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a test templates file
        self.test_templates = {
            "ports": {
                "80": {
                    "service": "http",
                    "description": "HTTP Web Server",
                    "nmap": "nmap -sV -p 80 -sC --script=http-* {target}",
                    "metasploit": [
                        "use auxiliary/scanner/http/http_version"
                    ],
                    "manual": [
                        "curl -v http://{target}/"
                    ]
                },
                "unknown": {
                    "service": "unknown",
                    "description": "Unknown service",
                    "nmap": "nmap -sV -p {port} -sC {target}",
                    "metasploit": [
                        "use auxiliary/scanner/discovery/tcp_port_scan"
                    ],
                    "manual": [
                        "nc -nv {target} {port}"
                    ]
                }
            },
            "services": {
                "http": "80"
            }
        }
        
        # Create a temporary test templates file
        self.test_templates_path = Path("test_templates.json")
        with open(self.test_templates_path, "w") as f:
            json.dump(self.test_templates, f)
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove the test templates file
        if self.test_templates_path.exists():
            os.remove(self.test_templates_path)
    
    def test_load_templates(self):
        """Test loading templates from file."""
        templates = enumcsh.load_templates(self.test_templates_path)
        self.assertEqual(templates["ports"]["80"]["service"], "http")
        self.assertEqual(templates["services"]["http"], "80")
    
    @patch("enumcsh.console")
    def test_display_port_info_known_port(self, mock_console):
        """Test displaying information for a known port."""
        enumcsh.display_port_info("80", self.test_templates, "192.168.1.1")
        # Check that console.print was called (we can't easily check the exact output)
        self.assertTrue(mock_console.print.called)
    
    @patch("enumcsh.console")
    def test_display_port_info_unknown_port(self, mock_console):
        """Test displaying information for an unknown port."""
        enumcsh.display_port_info("12345", self.test_templates, "192.168.1.1")
        # Check that console.print was called with a warning about unknown port
        mock_console.print.assert_any_call(
            "[bold yellow]No specific template for port 12345. Using generic template.[/bold yellow]"
        )
    
    @patch("enumcsh.subprocess.run")
    @patch("enumcsh.typer.confirm", return_value=True)
    @patch("enumcsh.console")
    def test_execute_command(self, mock_console, mock_confirm, mock_run):
        """Test executing a command with confirmation."""
        enumcsh.execute_command("echo test")
        mock_confirm.assert_called_once()
        mock_run.assert_called_once_with("echo test", shell=True)
    
    @patch("enumcsh.subprocess.run")
    @patch("enumcsh.console")
    def test_run_nmap_scan(self, mock_console, mock_run):
        """Test running an Nmap scan."""
        # Mock the subprocess.run result
        mock_process = MagicMock()
        mock_process.stdout = """
        Starting Nmap 7.80 ( https://nmap.org )
        Nmap scan report for localhost (127.0.0.1)
        Host is up (0.00026s latency).
        Not shown: 997 closed ports
        PORT   STATE SERVICE
        22/tcp open  ssh
        80/tcp open  http
        443/tcp open  https
        
        Nmap done: 1 IP address (1 host up) scanned in 0.05 seconds
        """
        mock_run.return_value = mock_process
        
        ports = enumcsh.run_nmap_scan("127.0.0.1")
        self.assertEqual(ports, ["22", "80", "443"])

if __name__ == "__main__":
    unittest.main()