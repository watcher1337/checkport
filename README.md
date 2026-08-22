
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

---

## 📖 Usage

```bash
checkport -c 8080          # Check if port is in use
checkport -k 8080          # Kill process on port
checkport --list           # List all listening ports
checkport --scan 8000-8100 # Scan port range
checkport -h               # Show help
```

### Options

| Option | Description |
|--------|-------------|
| `-c, --check PORT` | Check if port is in use |
| `-k, --kill PORT` | Kill process on port |
| `--list` | List all listening ports |
| `--scan RANGE` | Scan port range (e.g., 8000-8100) |
| `--force` | Force kill process |
| `-v, --verbose` | Verbose output |
| `--no-color` | Disable colors |

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

## 📝 License

MIT

## 👤 Author

**watcher1337** · [GitHub](https://github.com/watcher1337)
```

---

## Even Shorter Version (One-Liner)

```markdown
# checkport

Port management tool for checking and killing processes.

## Install
```bash
pip install checkport
```

## Usage
```bash
checkport -c 8080  # Check port
checkport -k 8080  # Kill process on port
checkport --list   # List all ports
checkport --scan 8000-8100  # Scan range
```

[GitHub](https://github.com/watcher1337/checkport)
```

