#!/usr/bin/env python3
"""
PORT MANAGER v2.0
A tool to check and kill processes running on specific ports
Enhanced with fixtime-style architecture and features
"""

import os
import sys
import platform
import subprocess
import argparse
import socket
import threading
import time
import re
import warnings
from typing import Optional, Tuple, List, Dict, Any
from datetime import datetime
import concurrent.futures

# ============================================================
# Terminal Colors
# ============================================================

class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    BLACK = "\033[30m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

def supports_color():
    """Return True if terminal likely supports ANSI colors."""
    if os.getenv("NO_COLOR") is not None:
        return False
    if not hasattr(sys.stdout, "isatty"):
        return False
    if not sys.stdout.isatty():
        return False
    if platform.system().lower() == "windows":
        return (os.getenv("ANSICON") is not None or
                os.getenv("WT_SESSION") is not None or
                os.getenv("TERM_PROGRAM") == "vscode" or
                os.getenv("TERM") is not None)
    return True

USE_COLOR = supports_color()

def color(text, code):
    if not USE_COLOR:
        return str(text)
    return f"{code}{text}{Color.RESET}"

def bold(text): return color(text, Color.BOLD)
def red(text): return color(text, Color.RED)
def green(text): return color(text, Color.GREEN)
def yellow(text): return color(text, Color.YELLOW)
def blue(text): return color(text, Color.BLUE)
def cyan(text): return color(text, Color.CYAN)
def magenta(text): return color(text, Color.MAGENTA)
def dim(text): return color(text, Color.DIM)

def colorize_message(message):
    message = str(message)
    prefixes = (("[✓]", Color.GREEN), ("[✗]", Color.RED), ("[!]", Color.YELLOW))
    for prefix, prefix_color in prefixes:
        if message.startswith(prefix):
            colored_prefix = color(prefix, prefix_color)
            return f"{colored_prefix}{message[len(prefix):]}"
    return message

def cprint(*values, **kwargs):
    """Replacement for print() that colors known status prefixes."""
    if not values:
        print(**kwargs)
        return
    values = list(values)
    if isinstance(values[0], str):
        values[0] = colorize_message(values[0])
    print(*values, **kwargs)

def print_value(label, value, indent=4):
    """Print a label/value pair with cyan label and bold value."""
    spaces = " " * indent
    print(f"{spaces}{cyan(f'{label:<16}')}{bold(value)}")

def print_separator(char="=", length=60):
    print(dim(char * length))

# ============================================================
# Platform detection
# ============================================================

def detect_os():
    """Detect OS and architecture."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        return "windows"
    elif system == "darwin":
        if machine in ["arm64", "aarch64"]:
            return "darwin_arm"
        return "darwin"
    else:
        if machine in ["arm64", "aarch64", "armv7l", "armv8l"]:
            return "linux_arm"
        return "linux"

def is_admin():
    """Return True if running with admin/root privileges."""
    if OS_NAME == "windows":
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    else:
        try:
            return os.geteuid() == 0
        except AttributeError:
            return os.system("sudo -n true") == 0

OS_NAME = detect_os()
IS_ADMIN = is_admin()

# ============================================================
# Configuration
# ============================================================

MAX_WORKERS = 4
print_lock = threading.Lock()

# ============================================================
# Arguments
# ============================================================

parser = argparse.ArgumentParser(
    description="Port management tool for checking and killing processes on specific ports",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    usage="checkport [OPTIONS]",
    add_help=False,
    epilog="""
Examples:
  checkport -c 8080                  # Check if port 8080 is in use
  checkport -k 8080                  # Kill process on port 8080
  checkport -c 80 -v                 # Check port 80 with verbose output
  checkport -k 443 --force           # Force kill process on port 443
  checkport --list                   # List all listening ports
  checkport --scan 8000-8100         # Scan port range
""",
)

parser.add_argument("-h", action="help", default=argparse.SUPPRESS,
                   help="show this help message")
parser.add_argument("-c", "--check", type=int, metavar="PORT",
                   help="Check if a port is open and show process info")
parser.add_argument("-k", "--kill", type=int, metavar="PORT",
                   help="Kill the process running on the specified port")
parser.add_argument("-v", "--verbose", action="store_true",
                   help="Enable verbose output")
parser.add_argument("--force", action="store_true",
                   help="Force kill process (SIGKILL immediately)")
parser.add_argument("--list", action="store_true",
                   help="List all listening ports")
parser.add_argument("--scan", type=str, metavar="RANGE",
                   help="Scan port range (e.g., 8000-8100)")
parser.add_argument("--no-color", action="store_true",
                   help="Disable colored output")

args = parser.parse_args()

if args.no_color:
    USE_COLOR = False

# ============================================================
# Logging
# ============================================================

def log(msg, force=False):
    if args.verbose or force:
        with print_lock:
            cprint(msg)

# ============================================================
# Core Port Management
# ============================================================

class PortManager:
    def __init__(self):
        self.system = OS_NAME
        self.is_admin = IS_ADMIN
        
    def find_process_on_port(self, port: int) -> Optional[Tuple[str, str, str]]:
        """
        Find process using a specific port.
        Returns (pid, command, user) if found, None otherwise.
        """
        log(f"[*] Looking for process on port {port}")
        
        # Try lsof first (most reliable)
        try:
            result = subprocess.run(
                ['lsof', '-i', f':{port}', '-t'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.stdout.strip():
                pid = result.stdout.strip().split('\n')[0]
                # Get process info
                ps_result = subprocess.run(
                    ['ps', '-p', pid, '-o', 'comm=', '-o', 'user='],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if ps_result.stdout.strip():
                    parts = ps_result.stdout.strip().split()
                    if len(parts) >= 2:
                        command = parts[0]
                        user = parts[1]
                        log(f"[+] Found process {pid} ({command}) on port {port}")
                        return (pid, command, user)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
            
        # Fallback to netstat/ss
        try:
            if self.system == 'linux' or self.system == 'linux_arm':
                cmd = ['ss', '-tlnp', f'sport = :{port}']
            elif self.system.startswith('darwin'):
                cmd = ['netstat', '-anv', '-p', 'tcp']
            else:  # windows
                cmd = ['netstat', '-ano', '-p', 'TCP']
                
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            
            if self.system.startswith('linux'):
                # Parse ss output
                for line in result.stdout.split('\n'):
                    if f':{port}' in line and 'LISTEN' in line:
                        match = re.search(r'pid=(\d+)', line)
                        if match:
                            pid = match.group(1)
                            ps_result = subprocess.run(
                                ['ps', '-p', pid, '-o', 'comm=', '-o', 'user='],
                                capture_output=True,
                                text=True,
                                timeout=5
                            )
                            if ps_result.stdout.strip():
                                parts = ps_result.stdout.strip().split()
                                if len(parts) >= 2:
                                    command = parts[0]
                                    user = parts[1]
                                    log(f"[+] Found process {pid} ({command}) on port {port}")
                                    return (pid, command, user)
            elif self.system.startswith('darwin'):
                # Parse netstat output (macOS)
                for line in result.stdout.split('\n'):
                    if f'.{port}' in line and 'LISTEN' in line:
                        parts = line.split()
                        if len(parts) >= 9:
                            pid = parts[8] if parts[8].isdigit() else None
                            if pid:
                                ps_result = subprocess.run(
                                    ['ps', '-p', pid, '-o', 'comm=', '-o', 'user='],
                                    capture_output=True,
                                    text=True,
                                    timeout=5
                                )
                                if ps_result.stdout.strip():
                                    parts = ps_result.stdout.strip().split()
                                    if len(parts) >= 2:
                                        command = parts[0]
                                        user = parts[1]
                                        log(f"[+] Found process {pid} ({command}) on port {port}")
                                        return (pid, command, user)
            else:  # Windows
                for line in result.stdout.split('\n'):
                    if f':{port}' in line and 'LISTENING' in line:
                        parts = line.split()
                        if len(parts) >= 5:
                            pid = parts[4] if parts[4].isdigit() else None
                            if pid:
                                try:
                                    ps_result = subprocess.run(
                                        ['tasklist', '/FI', f'PID eq {pid}'],
                                        capture_output=True,
                                        text=True,
                                        timeout=5
                                    )
                                    if ps_result.stdout:
                                        lines = ps_result.stdout.split('\n')
                                        if len(lines) > 3:
                                            proc_info = lines[3].split()
                                            if len(proc_info) >= 2:
                                                command = proc_info[0]
                                                user = "N/A"
                                                log(f"[+] Found process {pid} ({command}) on port {port}")
                                                return (pid, command, user)
                                except Exception:
                                    pass
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
            
        # Last fallback: try fuser
        try:
            result = subprocess.run(
                ['fuser', f'{port}/tcp'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.stdout.strip():
                pid = result.stdout.strip().split()[0]
                ps_result = subprocess.run(
                    ['ps', '-p', pid, '-o', 'comm=', '-o', 'user='],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if ps_result.stdout.strip():
                    parts = ps_result.stdout.strip().split()
                    if len(parts) >= 2:
                        command = parts[0]
                        user = parts[1]
                        log(f"[+] Found process {pid} ({command}) on port {port}")
                        return (pid, command, user)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
            
        log(f"[-] No process found on port {port}")
        return None
        
    def check_port(self, port: int) -> bool:
        """
        Check if port is in use and display process info.
        Returns True if port is in use, False otherwise.
        """
        log(f"[*] Checking port {port}")
        
        result = self.find_process_on_port(port)
        
        print()
        print_separator()
        if result:
            pid, command, user = result
            cprint(f"[✓] Port {port} is IN USE")
            print_separator()
            print_value("COMMAND", command)
            print_value("PID", pid)
            print_value("USER", user)
            print_separator()
            
            # Show detailed lsof output if available
            if self.system.startswith('darwin') or self.system.startswith('linux'):
                try:
                    lsof_result = subprocess.run(
                        ['lsof', '-i', f':{port}'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if lsof_result.stdout:
                        lines = lsof_result.stdout.split('\n')
                        if len(lines) > 1:
                            print("\nDetailed info:")
                            print(lines[0])  # Header
                            if len(lines) > 2:
                                print(lines[1])  # First data line
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    pass
            return True
        else:
            cprint(f"[✓] Port {port} is FREE")
            print_separator()
            return False
            
    def kill_process_on_port(self, port: int) -> bool:
        """
        Kill process running on specified port.
        Returns True if successful, False otherwise.
        """
        # Check if port is privileged
        if port < 1024 and not self.is_admin:
            cprint(f"[!] Port {port} is a privileged port (below 1024)")
            cprint("[!] You may need to run with sudo for proper operation")
            
        result = self.find_process_on_port(port)
        
        if not result:
            cprint(f"[✓] No process found on port {port}")
            return False
            
        pid, command, user = result
        cprint(f"[*] Found process {pid} ({command}) on port {port}")
        
        try:
            if args.force:
                # Force kill immediately
                if self.system == "windows":
                    subprocess.run(['taskkill', '/F', '/PID', pid], check=True)
                else:
                    os.kill(int(pid), 9)  # SIGKILL
                cprint(f"[✓] Successfully force killed process {pid} on port {port}")
                return True
                
            # Try gentle kill first (SIGTERM)
            if self.system == "windows":
                subprocess.run(['taskkill', '/PID', pid], check=True)
            else:
                os.kill(int(pid), 15)  # SIGTERM
                
            # Wait a moment and check if process is still running
            time.sleep(0.5)
            
            # Check if process still exists
            if self.system == "windows":
                try:
                    subprocess.run(['tasklist', '/FI', f'PID eq {pid}'], 
                                 capture_output=True, check=True)
                except Exception:
                    cprint(f"[✓] Successfully killed process {pid} on port {port}")
                    return True
            else:
                try:
                    os.kill(int(pid), 0)  # Check if process exists
                    # Process still exists, try SIGKILL
                    cprint("[!] Process didn't terminate gracefully, forcing kill...")
                    os.kill(int(pid), 9)  # SIGKILL
                    cprint(f"[✓] Successfully killed process {pid} on port {port}")
                    return True
                except OSError:
                    # Process is gone
                    cprint(f"[✓] Successfully killed process {pid} on port {port}")
                    return True
                    
        except PermissionError:
            cprint("[✗] Permission denied. Try running with sudo")
            return False
        except ProcessLookupError:
            cprint(f"[✓] Process {pid} was already terminated")
            return True
        except Exception as e:
            cprint(f"[✗] Error killing process: {e}")
            return False
            
    def list_listening_ports(self) -> List[Dict[str, Any]]:
        """List all listening ports with process info."""
        ports = []
        
        try:
            if self.system.startswith('linux'):
                cmd = ['ss', '-tlnp']
            elif self.system.startswith('darwin'):
                cmd = ['netstat', '-anv', '-p', 'tcp']
            else:  # windows
                cmd = ['netstat', '-ano', '-p', 'TCP']
                
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            for line in result.stdout.split('\n'):
                if 'LISTEN' in line:
                    port_match = re.search(r':(\d+)\s', line)
                    if port_match:
                        port = int(port_match.group(1))
                        process_info = self.find_process_on_port(port)
                        ports.append({
                            'port': port,
                            'pid': process_info[0] if process_info else 'N/A',
                            'command': process_info[1] if process_info else 'N/A',
                            'user': process_info[2] if process_info else 'N/A'
                        })
        except Exception as e:
            log(f"[-] Error listing ports: {e}")
            
        return ports
        
    def scan_port_range(self, start: int, end: int) -> List[int]:
        """Scan a range of ports and return open ones."""
        open_ports = []
        
        cprint(f"[*] Scanning ports {start}-{end}...")
        
        def scan_single_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex(('127.0.0.1', port))
                sock.close()
                if result == 0:
                    return port
            except Exception:
                pass
            return None
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(scan_single_port, port): port 
                      for port in range(start, end + 1)}
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
                    process_info = self.find_process_on_port(result)
                    if process_info:
                        cprint(f"[+] Port {result} is open (PID: {process_info[0]}, {process_info[1]})")
                    else:
                        cprint(f"[+] Port {result} is open")
                        
        return open_ports

# ============================================================
# Main
# ============================================================

def main():
    """Main entry point for the checkport tool."""
    # Display system info in verbose mode
    if args.verbose:
        cprint(f"[*] OS: {OS_NAME}")
        cprint(f"[*] Architecture: {platform.machine()}")
        cprint(f"[*] Admin privileges: {IS_ADMIN}")
    
    pm = PortManager()
    
    # Handle list operation
    if args.list:
        cprint("\n[🔄] Listing all listening ports...")
        print_separator()
        ports = pm.list_listening_ports()
        if ports:
            cprint(f"[+] Found {len(ports)} listening ports:")
            print_separator()
            print(f"{'PORT':<8} {'PID':<8} {'USER':<12} COMMAND")
            print_separator()
            for p in sorted(ports, key=lambda x: x['port']):
                print(f"{p['port']:<8} {p['pid']:<8} {p['user']:<12} {p['command']}")
            print_separator()
        else:
            cprint("[!] No listening ports found")
        return
        
    # Handle scan operation
    if args.scan:
        try:
            if '-' in args.scan:
                start, end = map(int, args.scan.split('-'))
                if start > end:
                    start, end = end, start
                if start < 1 or end > 65535:
                    cprint("[✗] Port range must be between 1 and 65535")
                    sys.exit(1)
                open_ports = pm.scan_port_range(start, end)
                if open_ports:
                    cprint(f"\n[+] Found {len(open_ports)} open ports: {open_ports}")
                else:
                    cprint("\n[!] No open ports found in range")
            else:
                cprint("[✗] Invalid port range format. Use start-end (e.g., 8000-8100)")
                sys.exit(1)
        except ValueError:
            cprint("[✗] Invalid port range. Use numeric values (e.g., 8000-8100)")
            sys.exit(1)
        return
        
    # Handle check operation
    if args.check:
        port = args.check
        if not (1 <= port <= 65535):
            cprint(f"[✗] Invalid port number: {port}. Must be between 1 and 65535")
            sys.exit(1)
        in_use = pm.check_port(port)
        sys.exit(0 if in_use else 1)
        
    # Handle kill operation
    if args.kill:
        port = args.kill
        if not (1 <= port <= 65535):
            cprint(f"[✗] Invalid port number: {port}. Must be between 1 and 65535")
            sys.exit(1)
        success = pm.kill_process_on_port(port)
        sys.exit(0 if success else 1)
        
    # No arguments provided
    parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        cprint(f"\n[✗] Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)