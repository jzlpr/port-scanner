#!/usr/bin/env python3
"""Banner grab – fångar tjänstebanner via TCP."""

import socket
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
}


def grab_banner(
    host: str, port: int, timeout: float = 5.0, payload: bytes | None = None
) -> str | None:
    """Ansluter till host:port och läser banner."""
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            if payload:
                s.sendall(payload)
            s.settimeout(timeout)
            chunks = []
            try:
                while True:
                    data = s.recv(4096)
                    if not data:
                        break
                    chunks.append(data)
                    if len(b"".join(chunks)) > 4096:
                        break
            except socket.timeout:
                pass
            banner = b"".join(chunks).decode("utf-8", errors="replace").strip()
            return banner if banner else None
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        return f"[ERROR] {e}"


def main():
    parser = argparse.ArgumentParser(description="Banner grab (TCP)")
    parser.add_argument("host", help="Målhost (IP eller domän)")
    parser.add_argument(
        "ports", nargs="*", type=int, help="Porter (default: vanliga porter)"
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=5.0,
        help="Timeout i sekunder (default: 5)",
    )
    parser.add_argument(
        "-p",
        "--payload",
        type=str,
        default=None,
        help="Valfri payload att skicka (t.ex. 'GET / HTTP/1.0\\r\\n\\r\\n')",
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="Lista vanliga porter och avsluta"
    )
    args = parser.parse_args()

    if args.list:
        for port, name in sorted(COMMON_PORTS.items()):
            print(f"  {port:<6} {name}")
        return

    ports = args.ports if args.ports else sorted(COMMON_PORTS.keys())
    payload = (
        args.payload.encode().decode("unicode_escape").encode("latin-1")
        if args.payload
        else None
    )

    print(f"[*] Banner grab mot {args.host} – {len(ports)} port(er)\n")

    with ThreadPoolExecutor(max_workers=min(len(ports), 20)) as pool:
        futures = {
            pool.submit(grab_banner, args.host, p, args.timeout, payload): p
            for p in ports
        }
        results = {}
        for future in as_completed(futures):
            port = futures[future]
            results[port] = future.result()

    for port in sorted(results):
        name = COMMON_PORTS.get(port, "unknown")
        banner = results[port]
        if banner and not banner.startswith("[ERROR]"):
            print(f"  [{port}/{name}]")
            for line in banner.splitlines()[:10]:
                print(f"    {line}")
            print()
        elif banner:
            print(f"  [{port}/{name}] {banner}\n")


if __name__ == "__main__":
    main()
