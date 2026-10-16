import sys
import nmapthon2 as nm2


def run_port_scanner(target_ip, ports="1-1024"):
    print(f"[*] Initializing Nmap scan against target: {target_ip} (Ports: {ports})")

    try:
        scanner = nm2.NmapScanner()
        result = scanner.scan(targets=target_ip, ports=ports, arguments="-sS -sV -T4")

        if not result:
            print("[-] Scan failed or returned no results.")
            return

        print("[+] Scan completed successfully.\n")

        for host in result:
            host_ip = getattr(host, "ipv4", str(host))

            try:
                names = host.hostnames()
                hostname = names[0] if names else "No hostname"
            except Exception:
                hostname = "No hostname"

            host_state = getattr(host, "state", "up")
            print(f"Host: {host_ip} ({hostname}) - Status: {host_state}")

            # --- Diagnostic: Try multiple methods to fetch ports ---
            ports_found = []
            for method_name in ["ports", "get_ports", "open_ports", "all_ports"]:
                if hasattr(host, method_name):
                    attr = getattr(host, method_name)
                    try:
                        # Try calling it as a method
                        ports_found = attr() if callable(attr) else attr
                        if ports_found:
                            print(
                                f"    [DEBUG] Successfully fetched ports using host.{method_name}()"
                            )
                            break
                    except TypeError:
                        try:
                            # Try with protocol argument
                            ports_found = attr(protocol="tcp")
                            if ports_found:
                                print(
                                    f"    [DEBUG] Successfully fetched ports using host.{method_name}(protocol='tcp')"
                                )
                                break
                        except Exception:
                            pass

            # If still nothing, inspect available attributes/methods on the host object for debugging
            if not ports_found:
                print(
                    "    [DEBUG] No ports found via standard methods. Inspecting host object properties:"
                )
                print(
                    f"    Available host attributes/methods: {[m for m in dir(host) if not m.startswith('_')]}"
                )
                print("    No open TCP ports found in the specified range.\n")
                continue

            print("\n    PORT\tSTATE\tSERVICE")
            print("    ----\t-----\t-------")
            for port in ports_found:
                # Handle both object-based ports and dictionary-based ports
                p_num = getattr(port, "port", None) or (
                    port.get("port") if isinstance(port, dict) else port
                )
                p_state = getattr(port, "state", None) or (
                    port.get("state") if isinstance(port, dict) else "unknown"
                )
                p_proto = getattr(port, "protocol", "tcp")

                service = getattr(port, "service", None)
                if service:
                    service_name = getattr(service, "name", "unknown")
                elif isinstance(port, dict) and "service" in port:
                    service_name = port["service"].get("name", "unknown")
                else:
                    service_name = "unknown"

                if p_state == "open":
                    print(f"    {p_num}/{p_proto}\t{p_state}\t{service_name}")
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
