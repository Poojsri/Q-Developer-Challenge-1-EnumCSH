# enumCSh Quick Start Guide

This guide will help you get started with enumCSh quickly.

## Installation

### Windows

```bash
# Clone the repository
git clone https://github.com/yourusername/enumcsh.git
cd enumcsh

# Install with pip
pip install --user -e .
```

### Linux/macOS

```bash
# Clone the repository
git clone https://github.com/yourusername/enumcsh.git
cd enumcsh

# Install with pip
pip3 install -e .
```

## Basic Usage

### Enumerate a specific port

```bash
enumcsh port --port 80 --target 192.168.1.10
```

### Enumerate a specific service

```bash
enumcsh service --service http --target 192.168.1.10
```

### Run a scan

```bash
enumcsh scan --target 192.168.1.10
```

### Interactive mode

```bash
enumcsh interactive
```

## If the command is not found

If you can't run `enumcsh` directly, try:

```bash
# Windows
python c:\path\to\enumcsh.py interactive

# Linux/macOS
python3 /path/to/enumcsh.py interactive
```

Or use the provided batch file on Windows:

```bash
c:\path\to\enumcsh-run.bat interactive
```