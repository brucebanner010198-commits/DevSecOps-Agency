#!/usr/bin/env python3
"""
Start one or more servers, wait for them to be ready, run a command, then clean up.

Agency-hardened variant (v0.3.5):
  - Original Anthropic skill used subprocess.Popen(shell=True) to support
    composite commands like "cd backend && python server.py". Agency posture
    ("injection-resistant, hard to break into") does not permit shell=True in
    imported scripts, so the CLI has been reshaped to pass per-server --cwd
    separately and run the server command through shlex.split(..., posix=True)
    with shell=False.

Usage:
    # Single server
    python scripts/with_server.py --server "npm run dev" --port 5173 -- python automation.py
    python scripts/with_server.py --server "npm start" --port 3000 -- python test.py

    # Multiple servers (use --cwd to run a server from a specific directory)
    python scripts/with_server.py \
      --server "python server.py" --cwd backend --port 3000 \
      --server "npm run dev"     --cwd frontend --port 5173 \
      -- python test.py

Security notes:
  - shell=False prevents shell metacharacter injection via the --server value.
  - If you need a shell-builtin (&&, ||, |, redirection, globbing), wrap it in
    a dedicated script file and point --server at that script. Do NOT route
    untrusted input through --server.
"""

import argparse
import os
import shlex
import socket
import subprocess
import sys
import time


def is_server_ready(port, timeout=30):
    """Wait for server to be ready by polling the port."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(('localhost', port), timeout=1):
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.5)
    return False


def main():
    parser = argparse.ArgumentParser(description='Run command with one or more servers')
    parser.add_argument('--server', action='append', dest='servers', required=True,
                        help='Server command (can be repeated). Parsed with shlex.split, shell=False.')
    parser.add_argument('--port', action='append', dest='ports', type=int, required=True,
                        help='Port for each server (must match --server count)')
    parser.add_argument('--cwd', action='append', dest='cwds', default=None,
                        help='Working directory for each server (optional). If any --cwd is given, it must match --server count; missing entries default to the current directory.')
    parser.add_argument('--timeout', type=int, default=30, help='Timeout in seconds per server (default: 30)')
    parser.add_argument('command', nargs=argparse.REMAINDER, help='Command to run after server(s) ready')

    args = parser.parse_args()

    # Remove the '--' separator if present
    if args.command and args.command[0] == '--':
        args.command = args.command[1:]

    if not args.command:
        print("Error: No command specified to run")
        sys.exit(1)

    if len(args.servers) != len(args.ports):
        print("Error: Number of --server and --port arguments must match")
        sys.exit(1)

    # Normalize --cwd list to the same length, filling with None (→ inherit cwd).
    cwds = args.cwds or []
    if cwds and len(cwds) != len(args.servers):
        print("Error: Number of --cwd values must match --server count (or be omitted entirely)")
        sys.exit(1)
    while len(cwds) < len(args.servers):
        cwds.append(None)

    servers = []
    for cmd, port, cwd in zip(args.servers, args.ports, cwds):
        argv = shlex.split(cmd, posix=True)
        if not argv:
            print(f"Error: empty --server command for port {port}")
            sys.exit(1)
        servers.append({'argv': argv, 'port': port, 'cwd': cwd, 'raw': cmd})

    server_processes = []

    try:
        for i, server in enumerate(servers):
            print(f"Starting server {i+1}/{len(servers)}: {server['raw']}"
                  + (f" (cwd={server['cwd']})" if server['cwd'] else ""))

            # shell=False so --server cannot inject shell metacharacters.
            process = subprocess.Popen(
                server['argv'],
                shell=False,
                cwd=server['cwd'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            server_processes.append(process)

            print(f"Waiting for server on port {server['port']}...")
            if not is_server_ready(server['port'], timeout=args.timeout):
                raise RuntimeError(
                    f"Server failed to start on port {server['port']} within {args.timeout}s"
                )

            print(f"Server ready on port {server['port']}")

        print(f"\nAll {len(servers)} server(s) ready")
        print(f"Running: {' '.join(args.command)}\n")
        result = subprocess.run(args.command)
        sys.exit(result.returncode)

    finally:
        print(f"\nStopping {len(server_processes)} server(s)...")
        for i, process in enumerate(server_processes):
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            print(f"Server {i+1} stopped")
        print("All servers stopped")


if __name__ == '__main__':
    main()
