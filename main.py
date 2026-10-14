import nmapthon2 as nm2

scanner = nm2.NmapScanner()

# Who wants the script kiddie output?
result = scanner.scan('192.168.1.0/24', output='kiddie')