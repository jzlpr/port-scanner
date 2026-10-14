import sys
from nmapthon2 import NmapScan

def run_port_scanner(target_ip, ports="1-1024"):
    print(f"[*] Initializing Nmap scan against target: {target_ip} (Ports: {ports})")
    
    try:
        # Initialize and run an Nmap scan (SYN scan by default with service detection if needed)
        # Note: Depending on privileges, SYN scans (-sS) require root/administrator permissions.
        scan = NmapScan(targets=target_ip, ports=ports, arguments="-sS -T4")
        
        # Check if the scan completed successfully
        if not scan.is_successful():
            print("[-] Scan failed or was interrupted.")
            return

        print(f"[+] Scan completed in {scan.elapsed()} seconds.\n")

        # Iterate over discovered hosts
        for host in scan.hosts():
            print(f"Host: {host} ({scan.hostname(host)}) - Status: {scan.state(host)}")
            
            # Check open TCP ports
            open_ports = scan.open_ports(host, protocol="tcp")
            if not open_ports:
                print("    No open TCP ports found in the specified range.")
                continue

            print("\n    PORT\tSTATE\tSERVICE")
            print("    ----\t-----\t-------")
            for port in open_ports:
                service = scan.service(host, port, protocol="tcp")
                service_name = service.get('name', 'unknown') if service else 'unknown'
                print(f"    {port}/tcp\topen\t{service_name}")

    except Exception as e:
        print(f"[-] An error occurred during the scan: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Example target (safe local testing or external permitted targets)
    target = input("Enter target IP or hostname (default: 127.0.0.1): ").strip()
    if not target:
        target = "127.0.0.1"
        
    port_range = input("Enter port range (default: 22,80,443 or 1-1024): ").strip()
    if not port_range:
        port_range = "22,80,443"

    run_port_scanner(target, port_range)