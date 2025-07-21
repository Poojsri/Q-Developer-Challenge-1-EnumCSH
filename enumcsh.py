#!/usr/bin/env python3
"""
enumCSh - A CLI tool that automates and simplifies port enumeration for penetration testing.
Functions as an interactive cheatsheet on the command line for known and unknown ports.
"""

# ASCII Art Banner
ASCII_BANNER = r"""
  _____                          _____  _____ _     
 |  ___|                        /  __ \/  ___| |    
 | |__ _ __  _   _ _ __ ___    | /  \/\ `--.| |__  
 |  __| '_ \| | | | '_ ` _ \   | |     `--. \ '_ \ 
 | |__| | | | |_| | | | | | |  | \__/\/\__/ / | | |
 \____/_| |_|\__,_|_| |_| |_|   \____/\____/|_| |_|
                                                    
         Port Enumeration Cheatsheet CLI
         v0.1.0 - Happy Hacking!
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax

# Initialize Typer app and Rich console
app = typer.Typer(help="Port enumeration cheatsheet CLI tool")
console = Console()

# Default templates file path
DEFAULT_TEMPLATES_PATH = Path(os.path.dirname(os.path.abspath(__file__))) / "templates.json"

def load_templates(templates_path: Path = DEFAULT_TEMPLATES_PATH) -> Dict[str, Any]:
    """Load enumeration templates from JSON file."""
    try:
        with open(templates_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] Templates file not found at {templates_path}")
        console.print("Creating default templates file...")
        create_default_templates(templates_path)
        with open(templates_path, "r") as f:
            return json.load(f)

def create_default_templates(templates_path: Path) -> None:
    """Create default templates file if it doesn't exist."""
    default_templates = {
        "ports": {
            "21": {
                "service": "ftp",
                "description": "File Transfer Protocol",
                "nmap": "nmap -sV -p 21 -sC --script=ftp-* {target}",
                "metasploit": [
                    "use auxiliary/scanner/ftp/ftp_version",
                    "use auxiliary/scanner/ftp/anonymous"
                ],
                "manual": [
                    "ftp {target}",
                    "Try anonymous:anonymous login",
                    "Check if PUT/GET commands are allowed"
                ]
            },
            "22": {
                "service": "ssh",
                "description": "Secure Shell",
                "nmap": "nmap -sV -p 22 -sC --script=ssh-* {target}",
                "metasploit": [
                    "use auxiliary/scanner/ssh/ssh_version",
                    "use auxiliary/scanner/ssh/ssh_enumusers"
                ],
                "manual": [
                    "ssh -v {target}",
                    "Check for weak credentials",
                    "Try username enumeration"
                ]
            },
            "23": {
                "service": "telnet",
                "description": "Telnet",
                "nmap": "nmap -sV -p 23 -sC --script=telnet-* {target}",
                "metasploit": [
                    "use auxiliary/scanner/telnet/telnet_version",
                    "use auxiliary/scanner/telnet/telnet_login"
                ],
                "manual": [
                    "telnet {target}",
                    "Check for default credentials",
                    "Look for banner information"
                ]
            },
            "25": {
                "service": "smtp",
                "description": "Simple Mail Transfer Protocol",
                "nmap": "nmap -sV -p 25 -sC --script=smtp-* {target}",
                "metasploit": [
                    "use auxiliary/scanner/smtp/smtp_version",
                    "use auxiliary/scanner/smtp/smtp_enum"
                ],
                "manual": [
                    "telnet {target} 25",
                    "EHLO localhost",
                    "VRFY admin",
                    "Check for user enumeration"
                ]
            },
            "80": {
                "service": "http",
                "description": "HTTP Web Server",
                "nmap": "nmap -sV -p 80 -sC --script=http-* {target}",
                "metasploit": [
                    "use auxiliary/scanner/http/http_version",
                    "use auxiliary/scanner/http/dir_scanner"
                ],
                "manual": [
                    "curl -v http://{target}/",
                    "gobuster dir -u http://{target}/ -w /usr/share/wordlists/dirb/common.txt",
                    "nikto -h http://{target}/"
                ]
            },
            "443": {
                "service": "https",
                "description": "HTTPS Web Server",
                "nmap": "nmap -sV -p 443 -sC --script=http-* --script=ssl-* {target}",
                "metasploit": [
                    "use auxiliary/scanner/http/http_version",
                    "use auxiliary/scanner/http/ssl"
                ],
                "manual": [
                    "curl -vk https://{target}/",
                    "gobuster dir -u https://{target}/ -w /usr/share/wordlists/dirb/common.txt -k",
                    "sslscan {target}"
                ]
            },
            "3306": {
                "service": "mysql",
                "description": "MySQL Database",
                "nmap": "nmap -sV -p 3306 -sC --script=mysql-* {target}",
                "metasploit": [
                    "use auxiliary/scanner/mysql/mysql_version",
                    "use auxiliary/scanner/mysql/mysql_login"
                ],
                "manual": [
                    "mysql -h {target} -u root -p",
                    "Check for default credentials",
                    "Try common username/password combinations"
                ]
            },
            "unknown": {
                "service": "unknown",
                "description": "Unknown service",
                "nmap": "nmap -sV -p {port} -sC {target}",
                "metasploit": [
                    "use auxiliary/scanner/discovery/udp_sweep",
                    "use auxiliary/scanner/discovery/tcp_port_scan"
                ],
                "manual": [
                    "nc -nv {target} {port}",
                    "telnet {target} {port}",
                    "Try sending various protocol handshakes"
                ]
            }
        },
        "services": {
            "ftp": "21",
            "ssh": "22",
            "telnet": "23",
            "smtp": "25",
            "http": "80",
            "https": "443",
            "mysql": "3306"
        }
    }
    
    os.makedirs(os.path.dirname(templates_path), exist_ok=True)
    with open(templates_path, "w") as f:
        json.dump(default_templates, f, indent=4)
    console.print(f"[bold green]Created default templates at {templates_path}[/bold green]")

def display_port_info(port: str, templates: Dict[str, Any], target: Optional[str] = "target") -> None:
    """Display enumeration information for a specific port."""
    port_data = templates["ports"].get(port)
    
    if not port_data:
        console.print(f"[bold yellow]No specific template for port {port}. Using generic template.[/bold yellow]")
        port_data = templates["ports"]["unknown"]
        # Replace {port} placeholder in commands
        for key in ["nmap", "manual"]:
            if isinstance(port_data.get(key), str):
                port_data[key] = port_data[key].replace("{port}", port)
            elif isinstance(port_data.get(key), list):
                port_data[key] = [cmd.replace("{port}", port) for cmd in port_data[key]]
    
    # Create a table for the port information
    table = Table(title=f"Port {port} - {port_data['service']} ({port_data['description']})")
    
    # Display Nmap commands
    if "nmap" in port_data:
        nmap_cmd = port_data["nmap"].replace("{target}", target)
        table.add_row("Nmap", Syntax(nmap_cmd, "bash", theme="monokai"))
    
    # Display Metasploit commands
    if "metasploit" in port_data:
        msf_cmds = "\n".join(port_data["metasploit"])
        msf_cmds = msf_cmds.replace("{target}", target)
        table.add_row("Metasploit", Syntax(msf_cmds, "ruby", theme="monokai"))
    
    # Display manual commands
    if "manual" in port_data:
        manual_cmds = "\n".join(port_data["manual"])
        manual_cmds = manual_cmds.replace("{target}", target)
        table.add_row("Manual", Syntax(manual_cmds, "bash", theme="monokai"))
    
    console.print(table)

def execute_command(command: str) -> None:
    """Execute a shell command with user confirmation."""
    console.print(f"[bold yellow]About to execute:[/bold yellow] {command}")
    confirm = typer.confirm("Do you want to proceed?")
    if confirm:
        try:
            console.print(f"[bold green]Executing:[/bold green] {command}")
            subprocess.run(command, shell=True)
        except Exception as e:
            console.print(f"[bold red]Error executing command:[/bold red] {str(e)}")
    else:
        console.print("[bold yellow]Command execution cancelled.[/bold yellow]")

def run_nmap_scan(target: str, ports: Optional[str] = None) -> List[str]:
    """Run a quick Nmap scan and return discovered ports."""
    scan_cmd = f"nmap -T4 -F {target}"
    if ports:
        scan_cmd = f"nmap -T4 -p {ports} {target}"
    
    console.print(f"[bold green]Running scan:[/bold green] {scan_cmd}")
    
    try:
        result = subprocess.run(scan_cmd, shell=True, capture_output=True, text=True)
        output = result.stdout
        
        # Parse Nmap output to extract open ports
        open_ports = []
        for line in output.splitlines():
            if "/tcp" in line and "open" in line:
                port = line.split("/")[0].strip()
                open_ports.append(port)
        
        console.print(f"[bold green]Discovered open ports:[/bold green] {', '.join(open_ports)}")
        return open_ports
    except Exception as e:
        console.print(f"[bold red]Error running Nmap scan:[/bold red] {str(e)}")
        return []

def interactive_mode(templates: Dict[str, Any]) -> None:
    """Run the tool in interactive mode."""
    # Display ASCII banner
    console.print(f"[bold green]{ASCII_BANNER}[/bold green]")
    console.print(Panel.fit("Welcome to Interactive Mode", border_style="green"))
    
    target = typer.prompt("Enter target IP/hostname")
    
    while True:
        console.print("\n[bold]Choose an option:[/bold]")
        console.print("1. Enter port number")
        console.print("2. Enter service name")
        console.print("3. Run Nmap scan")
        console.print("4. Exit")
        
        choice = typer.prompt("Enter your choice", type=int)
        
        if choice == 1:
            port = typer.prompt("Enter port number")
            display_port_info(port, templates, target)
            
            # Ask if user wants to execute Nmap command
            nmap_cmd = templates["ports"].get(port, templates["ports"]["unknown"])["nmap"].replace("{target}", target)
            if "{port}" in nmap_cmd:
                nmap_cmd = nmap_cmd.replace("{port}", port)
            
            if typer.confirm("Do you want to execute the Nmap command?"):
                execute_command(nmap_cmd)
                
        elif choice == 2:
            service = typer.prompt("Enter service name").lower()
            if service in templates["services"]:
                port = templates["services"][service]
                display_port_info(port, templates, target)
            else:
                console.print(f"[bold red]Service '{service}' not found in templates.[/bold red]")
                
        elif choice == 3:
            ports = run_nmap_scan(target)
            for port in ports:
                display_port_info(port, templates, target)
                
        elif choice == 4:
            console.print("[bold green]Exiting enumCSh. Happy hacking![/bold green]")
            break
            
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")

@app.command()
def port(
    port: str = typer.Option(None, "--port", "-p", help="Port number to enumerate"),
    target: str = typer.Option("target", "--target", "-t", help="Target IP/hostname"),
    execute: bool = typer.Option(False, "--execute", "-e", help="Execute the Nmap command"),
    templates_path: Path = typer.Option(DEFAULT_TEMPLATES_PATH, "--templates", help="Path to templates JSON file")
):
    """Enumerate a specific port."""
    templates = load_templates(templates_path)
    display_port_info(port, templates, target)
    
    if execute:
        port_data = templates["ports"].get(port, templates["ports"]["unknown"])
        nmap_cmd = port_data["nmap"].replace("{target}", target)
        if "{port}" in nmap_cmd:
            nmap_cmd = nmap_cmd.replace("{port}", port)
        execute_command(nmap_cmd)

@app.command()
def service(
    service_name: str = typer.Option(None, "--service", "-s", help="Service name to enumerate"),
    target: str = typer.Option("target", "--target", "-t", help="Target IP/hostname"),
    execute: bool = typer.Option(False, "--execute", "-e", help="Execute the Nmap command"),
    templates_path: Path = typer.Option(DEFAULT_TEMPLATES_PATH, "--templates", help="Path to templates JSON file")
):
    """Enumerate a specific service."""
    templates = load_templates(templates_path)
    
    if service_name.lower() in templates["services"]:
        port = templates["services"][service_name.lower()]
        display_port_info(port, templates, target)
        
        if execute:
            port_data = templates["ports"][port]
            nmap_cmd = port_data["nmap"].replace("{target}", target)
            execute_command(nmap_cmd)
    else:
        console.print(f"[bold red]Service '{service_name}' not found in templates.[/bold red]")

@app.command()
def scan(
    target: str = typer.Option(..., "--target", "-t", help="Target IP/hostname to scan"),
    ports: str = typer.Option(None, "--ports", help="Ports to scan (e.g., '80,443,8080' or '1-1000')"),
    templates_path: Path = typer.Option(DEFAULT_TEMPLATES_PATH, "--templates", help="Path to templates JSON file")
):
    """Scan target and provide enumeration suggestions."""
    templates = load_templates(templates_path)
    discovered_ports = run_nmap_scan(target, ports)
    
    for port in discovered_ports:
        display_port_info(port, templates, target)

@app.command()
def interactive(
    templates_path: Path = typer.Option(DEFAULT_TEMPLATES_PATH, "--templates", help="Path to templates JSON file")
):
    """Run in interactive mode."""
    templates = load_templates(templates_path)
    interactive_mode(templates)

@app.callback()
def main():
    """enumCSh - A CLI tool for port enumeration cheatsheets."""
    # Display ASCII banner when the tool is launched
    console.print(f"[bold green]{ASCII_BANNER}[/bold green]")
    pass

if __name__ == "__main__":
    app()