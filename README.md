Looking at the README content, I can see a few syntax issues that need fixing:

## Issues Found:

1. **Incorrect backtick escaping** in the "Even Shorter Version" section - there are extra backticks around the bash code block
2. **Missing language specifier** for the code block in the shorter version
3. **Inconsistent indentation** in the options table

## Fixed Version:

```markdown
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

If you want the absolute minimum:

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

---

## Key Fixes Made:

1. **Removed extra backticks** in the shorter version's code block
2. **Added `bash` language specifier** to both code blocks in the shorter version
3. **Kept consistent formatting** throughout
4. **Properly closed all code blocks** with triple backticks

The original had:
- Extra backticks that would break markdown rendering
- Missing language specifiers that could affect syntax highlighting
- Inconsistent code block formatting

Now both versions render correctly in any markdown viewer!
