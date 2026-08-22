# checkport

[![GitHub release](https://img.shields.io/github/release/watcher1337/checkport.svg)](https://github.com/watcher1337/checkport/releases/latest)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/watcher1337/checkport/releases)

**Port management tool for checking and killing processes on specific ports.**

---

## 🚀 Quick Install

```bash
pip install checkport
# or
pipx install checkport
# or
uv tool install checkport
```
## 📖 Usage

```bash
checkport -c 8080          # Check if port is in use
checkport -k 8080          # Kill process on port
checkport --list           # List all listening ports
checkport --scan 8000-8100 # Scan port range
checkport -h               # Show help




## Options
```
Option	Description
-c, --check PORT	Check if port is in use
-k, --kill PORT	Kill process on port
--list	List all listening ports
--scan RANGE	Scan port range (e.g., 8000-8100)
--force	Force kill process
-v, --verbose	Verbose output
--no-color	Disable colors
