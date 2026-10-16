import sys
import nmapthon2 as nm2


def run_port_scanner(target_ip, ports="1-1024"):
    print(f"[*] Initializing Nmap scan against target: {target_ip} (Ports: {ports})")

    try:
        # Initialize the NmapScanner instance
        scanner = nm2.NmapScanner()

        # Execute the scan matching standard nmapthon2 implementation
        result = scanner.scan(targets=target_ip, ports=ports, arguments="-T4")

        if not result:
            print("[-] Scan failed or returned no results.")
            return

        print("[+] Scan completed successfully.\n")

        # Iterate through discovered hosts using nmapthon2 result objects
        for host in result:
            host_ip = getattr(host, "ipv4", None) or getattr(host, "ip", str(host))

            # Retrieve hostnames list safely using nmapthon2 host.hostnames()
            try:
                names = host.hostnames()
                hostname = names[0] if names else "No hostname"
            except Exception:
                hostname = "No hostname"

            host_state = getattr(host, "state", "up")
            print(f"Host: {host_ip} ({hostname}) - Status: {host_state}")

            # Fetch TCP ports using nmapthon2's native tcp_ports attribute/method
            tcp_ports_handler = getattr(host, "tcp_ports", None)
            ports_found = (
                tcp_ports_handler()
                if callable(tcp_ports_handler)
                else (tcp_ports_handler or [])
            )

            if not ports_found:
                print("    No open TCP ports found in the specified range.\n")
                continue

            print("\n    PORT\tSTATE\tSERVICE")
            print("    ----\t-----\t-------")
            for port in ports_found:
                # Correctly resolve port number from nmapthon2 Port object attributes
                p_num = (
                    getattr(port, "number", None)
                    or getattr(port, "port", None)
                    or getattr(port, "portid", None)
                    or (port.get("port") if isinstance(port, dict) else "unknown")
                )

                p_state = getattr(port, "state", None) or (
                    port.get("state") if isinstance(port, dict) else "unknown"
                )

                service = getattr(port, "service", None)
                if service:
                    service_name = getattr(service, "name", "unknown")
                elif isinstance(port, dict) and "service" in port:
                    service_name = port["service"].get("name", "unknown")
                else:
                    service_name = "unknown"

                if p_state == "open":
                    print(f"    {p_num}/tcp\topen\t{service_name}")
            print()

    except Exception as e:
        print(f"[-] An error occurred during the scan: {e}", file=sys.stderr)


if __name__ == "__main__":
    target = input("Enter target IP or hostname (default: 192.168.1.1): ").strip()
    if not target:
        target = "192.168.1.1"

    port_range = input("Enter port range (default: 1-1024): ").strip()
    if not port_range:
        port_range = "1-1024"

    run_port_scanner(target, port_range)
