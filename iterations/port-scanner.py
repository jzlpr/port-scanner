import sys
import nmapthon2 as nm2

def run_port_scanner(target_ip, ports="1-1024"):
    print(f"[*] Initializing Nmap scan against target: {target_ip} (Ports: {ports})")
    
    try:
        # Initialize the NmapScanner instance
        scanner = nm2.NmapScanner()
        
        # Execute the scan (-sS or -A requires root/administrator privileges)
        result = scanner.scan(targets=target_ip, ports=ports, arguments="-A -T4")
        
        if not result:
            print("[-] Scan failed or returned no results.")
            return

        print("[+] Scan completed successfully.\n")

        # Iterate through the discovered hosts in the NmapScanResult
        for host in result:
            host_ip = getattr(host, 'ipv4', str(host))
            
            # host.hostnames() is a method that returns a list of names
            try:
                names = host.hostnames()
                hostname = names[0] if names else "No hostname"
            except Exception:
                hostname = "No hostname"
            
            # Check status safely
            host_status = getattr(host, 'status', 'up')
            
            print(f"Host: {host_ip} ({hostname}) - Status: {host_status}")
            
            # Retrieve open ports if the method is available on the host object
            open_ports = []
            if hasattr(host, 'open_ports'):
                try:
                    open_ports = host.open_ports(protocol="tcp")
                except TypeError:
                    # Fallback if open_ports doesn't take arguments in some versions
                    open_ports = host.open_ports()

            if not open_ports:
                print("    No open TCP ports found in the specified range.\n")
                continue

            print("\n    PORT\tSTATE\tSERVICE")
            print("    ----\t-----\t-------")
            for port in open_ports:
                service_name = 'unknown'
                if hasattr(host, 'service'):
                    try:
                        service = host.service(port, protocol="tcp")
                    except TypeError:
                        service = host.service(port)
                    
                    if isinstance(service, dict):
                        service_name = service.get('name', 'unknown')
                    elif hasattr(service, 'name'):
                        service_name = service.name
                        
                print(f"    {port}/tcp\topen\t{service_name}")
            print()

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