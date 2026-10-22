#!/usr/bin/env python3
# ============================================================================
#  port-scanner.py - Network Port Scanner built on top of Nmap / nmapthon2
# ----------------------------------------------------------------------------
#  Purpose : Prompts the user for a target and a port range, runs an Nmap
#            scan through the nmapthon2 wrapper, and pretty-prints every
#            discovered host together with its open TCP ports and services.
#  Author  : port-scanner project
#  Usage   : python port-scanner.py   (interactive - asks for input)
#  Requires: nmap binary installed on the system + `pip install nmapthon2`
# ============================================================================

# Import the `sys` module - used here to write error messages to stderr (line: error handler below).
import sys

# Import the third-party `nmapthon2` library (aliased as `nm2`) - a Python wrapper around the Nmap scanner binary.
import nmapthon2 as nm2


# Define the main scanning function; it accepts a target IP/hostname and an optional port spec (default: 1-1024).
def run_port_scanner(target_ip, ports="1-1024"):
    # Print a status line announcing the scan start, the target, and the port range being scanned.
    print(f"[*] Initializing Nmap scan against target: {target_ip} (Ports: {ports})")

    # Begin a try/except block so any failure inside the scan (missing nmap, bad host, etc.) is handled gracefully.
    try:
        # Instantiate an NmapScanner object from nmapthon2 - this is the reusable wrapper around the nmap binary.
        scanner = nm2.NmapScanner()

        # Execute the scan: pass the target host, the port specification, and `-T4` (Nmap's "aggressive" timing template).
        # The returned `result` is an NmapScanResult - an iterable of Host objects discovered on the network.
        result = scanner.scan(targets=target_ip, ports=ports, arguments="-T4")

        # Guard clause: if the scan returned nothing (None / empty), report failure and exit the function early.
        if not result:
            # Inform the user (on stdout) that the scan produced no usable results.
            print("[-] Scan failed or returned no results.")
            # Stop processing - there is nothing to iterate over.
            return

        # If we reach this point the scan succeeded; print a confirmation followed by a blank line for spacing.
        print("[+] Scan completed successfully.\n")

        # Loop over every Host object contained in the scan result - one iteration per discovered machine.
        for host in result:
            # Resolve the host's IPv4 address; fall back to `ip`, and finally to the string form of the object.
            host_ip = getattr(host, "ipv4", None) or getattr(host, "ip", str(host))

            # Try to obtain a hostname for this host - the API call may raise, so wrap it defensively.
            try:
                # Call hostnames() which returns a list of hostnames discovered via reverse-DNS / Nmap.
                names = host.hostnames()
                # Use the first hostname if the list is non-empty; otherwise use the placeholder text.
                hostname = names[0] if names else "No hostname"
            # If anything went wrong while reading hostnames, fall back silently.
            except Exception:
                # Assign the placeholder so the report still prints cleanly.
                hostname = "No hostname"

            # Read the host's up/down state; default to "up" if the attribute is missing for any reason.
            host_state = getattr(host, "state", "up")
            # Print the host summary line: IP address, resolved hostname, and its state.
            print(f"Host: {host_ip} ({hostname}) - Status: {host_state}")

            # Fetch the TCP-port container for this host; it may be a method or a list depending on the API version.
            tcp_ports_handler = getattr(host, "tcp_ports", None)
            # If it is callable, call it to get the list of ports; otherwise use it directly (or an empty list if absent).
            ports_found = (
                tcp_ports_handler()
                if callable(tcp_ports_handler)
                else (tcp_ports_handler or [])
            )

            # If no TCP ports were reported for this host, say so and move on to the next host.
            if not ports_found:
                # Print the "no open ports" message plus a blank line to separate hosts visually.
                print("    No open TCP ports found in the specified range.\n")
                # `continue` jumps to the next iteration of the host loop.
                continue

            # Print the table header: column names for port number, state, and service name.
            print("\n    PORT\tSTATE\tSERVICE")
            # Print a dashed separator line directly under the header.
            print("    ----\t-----\t-------")
            # Iterate over every port object discovered on the current host.
            for port in ports_found:
                # Extract the numeric port identifier, trying several attribute names used across API versions,
                # and finally treating the item as a plain dict if that is what came back.
                p_num = (
                    getattr(
                        port, "number", None
                    )  # nmapthon2 Port objects expose `.number`
                    or getattr(port, "port", None)  # some versions expose `.port`
                    or getattr(port, "portid", None)  # raw XML uses `portid`
                    or (
                        port.get("port") if isinstance(port, dict) else "unknown"
                    )  # dict fallback
                )

                # Extract the port state ("open" / "filtered" / "closed") with the same defensive pattern.
                p_state = getattr(port, "state", None) or (
                    port.get("state")
                    if isinstance(port, dict)
                    else "unknown"  # dict fallback
                )

                # Attempt to read the Service object attached to this port.
                service = getattr(port, "service", None)
                # If a service object exists, pull its human-readable name.
                if service:
                    # `.name` holds e.g. "http", "ssh"; default to "unknown" if missing.
                    service_name = getattr(service, "name", "unknown")
                # If the port came back as a dict containing a "service" key instead…
                elif isinstance(port, dict) and "service" in port:
                    # …read the service name from that nested dictionary.
                    service_name = port["service"].get("name", "unknown")
                # Otherwise no service information is available at all.
                else:
                    # Fall back to the "unknown" placeholder.
                    service_name = "unknown"

                # Only report ports that Nmap determined are actually OPEN (skip closed/filtered ones).
                if p_state == "open":
                    # Print one aligned table row: port number / protocol, state, and service name.
                    print(f"    {p_num}/tcp\topen\t{service_name}")
            # After finishing this host's port table, print a blank line as a separator.
            print()

    # Catch ANY exception raised anywhere inside the try block above.
    except Exception as e:
        # Print the error message to stderr (not stdout) so failures are distinguishable in scripts.
        print(f"[-] An error occurred during the scan: {e}", file=sys.stderr)


# Standard Python entry-point guard: the code below only runs when the file is executed directly,
# not when it is imported as a module by another script.
if __name__ == "__main__":
    # Prompt the user for a target IP or hostname, stripping surrounding whitespace from the reply.
    target = input("Enter target IP or hostname (default: 192.168.1.1): ").strip()
    # If the user just pressed Enter (empty string), fall back to the default gateway example.
    if not target:
        # Assign the default target address.
        target = "192.168.1.1"

    # Prompt the user for the port range to scan (Nmap syntax like "1-1024" or "80,443"), trimmed of whitespace.
    port_range = input("Enter port range (default: 1-1024): ").strip()
    # If the user left it blank, use the standard well-known-ports range as the default.
    if not port_range:
        # Assign the default port range.
        port_range = "1-1024"

    # Finally, invoke the scanning function with the collected target and port range.
    run_port_scanner(target, port_range)
