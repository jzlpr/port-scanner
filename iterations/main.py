import nmapthon2 as nm2
from nmapthon2.ports import top_ports

scanner = nm2.NmapScanner()

# Take into account that only hosts that respond will be stored
result = scanner.scan('192.168.1.0/24', arguments='-sS -sV -T4')

# Get a list with all scanned hosts
hosts = result.scanned_hosts()

# Directly iterate through the NmapScanResult Object
for host in result:
    print(f'This is a host instance: {host}')

# Get a host by IPv4. This will return None if the host could not be scanned
one_host = result['192.168.0.1']

# Get a host by hostname. This will return None if the host could not be scanned
another_host = result['localhost']

# Check if a host has been scanned by IPv4 or hostname
if 'localhost' in result:
    print('We could scan localhost successfully!')

# You can also create an iterable if necessary
iterable_results = iter(result)