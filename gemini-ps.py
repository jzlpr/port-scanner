import sys
import nmapthon2 as nm2

def run_port_scanner(target_ip, ports="1-1024"):
    print(f"[*] Initializing Nmap scan against target: {target_ip} (Ports: {ports})")
    
    try:
        # Initialize the NmapScanner instance
        scanner = nm2.NmapScanner()
        
        # Execute the scan (-A or -sS requires root/administrator privileges)
        result = scanner.scan(targets=target_ip, ports=ports, arguments="-A -T4")
        
        if not result:
            print("[-] Scan failed or returned no results.")
            return

        print("[+] Scan completed successfully.\n")

        # nmapthon2 scan results are directly iterable to loop through discovered hosts
        for host in result:
            host_ip = getattr(host, 'ipv4', None) or getattr(host, 'address', str(host))
            host_state = getattr(host, 'status', 'unknown')
            hostname = getattr(host, 'hostname', 'No hostname')
            
            print(f"Host: {host_ip} ({hostname}) - Status: {host_state}")
            
            # Check open TCP ports for the discovered host
            open_ports = host.open_ports(protocol="tcp") if hasattr(host, 'open_ports') else []
            if not open_ports:
                print("    No open TCP ports found in the specified range.")
                continue

            print("\n    PORT\tSTATE\tSERVICE")
            print("    ----\t-----\t-------")
            for port in open_ports:
                service = host.service(port, protocol="tcp") if hasattr(host, 'service') else None
                service_name = service.get('name', 'unknown') if isinstance(service, dict) else getattr(service, 'name', 'unknown')
                print(f"    {port}/tcp\topen\t{service_name}")

    except Exception as e:
        print(f"[-] An error occurred during the scan: {e}", file=sys.stderr)

if __name__ == "__main__":
    target = input("Enter target IP or hostname (default: 192.168.1.1): ").strip()
    if not target:
        target = "192.168.1.1"
        
    port_range = input("Enter port range (default: 22,80,443 or 1-1024): ").strip()
    if not port_range:
        port_range = "22,80,443"

    run_port_scanner(target, port_range)
