# checkport

[![GitHub release](https://img.shields.io/github/release/watcher1337/checkport.svg)](https://github.com/watcher1337/checkport/releases/latest)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/watcher1337/checkport/releases)

**A powerful port management tool for checking and killing processes running on specific ports.**

**Cross-platform and easy to use.**

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Install](#-quick-install)
- [Usage](#-usage)
- [Examples](#-examples)
- [Building from Source](#-building-from-source)

---

## ✨ Features

- 🔍 **Port Checking** – Check if a port is in use and get process information
- 🔪 **Process Killing** – Kill processes running on specific ports with graceful termination
- 📋 **List Ports** – Display all listening ports with process details
- 🔎 **Port Scanning** – Scan a range of ports to find open ones
- 🖥️ **Cross-platform** – Windows, Linux, macOS (x64 & ARM64)
- 🎨 **Colored Output** – Beautiful terminal output with status indicators
- 🚀 **Fast** – Concurrent scanning for quick results
- 💪 **Force Kill** – Force kill processes when graceful termination fails

---

## 🚀 Quick Install

### Using pip / pipx

```bash
# Install using pip
pip install checkport

# Install using pipx (recommended for CLI tools)
pipx install checkport

# Install using uv
uv tool install checkport


