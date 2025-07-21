#!/bin/bash

# Installation script for enumCSh

echo "Installing enumCSh..."

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install Python3 and pip3 first."
    exit 1
fi

# Check if Nmap is installed
if ! command -v nmap &> /dev/null; then
    echo "Warning: Nmap is not installed. Some features may not work."
    echo "To install Nmap on Kali Linux, run: sudo apt-get install nmap"
fi

# Install the package
pip3 install -e .

echo "Installation complete!"
echo "You can now use enumCSh by running: enumcsh"
echo "For help, run: enumcsh --help"