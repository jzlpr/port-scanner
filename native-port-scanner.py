import socket
from concurrent.futures import ThreadPoolExecutor


def scan_port(target, port):
    """Försöker ansluta till en specifik port via TCP."""
    try:
        # Skapa ett TCP-socket-objekt
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Sätt en timeout på 1 sekund så att vi inte fastnar på stängda portar
            s.settimeout(1.0)

            # connect_ex returnerar 0 om anslutningen lyckades (porten är öppen)
            result = s.connect_ex((target, port))
            if result == 0:
                return port
    except Exception:
        pass
    return None


def main():
    print("--- Enkel Port Scanner (Endast Standardbibliotek) ---")

    # 1. Samla in användarindata
    target = input("Ange mål-IP eller hostname (standard: 127.0.0.1): ").strip()
    if not target:
        target = "127.0.0.1"

    try:
        start_input = input("Startport (standard: 1): ").strip()
        start_port = int(start_input) if start_input else 1

        end_input = input("Slutport (standard: 1024): ").strip()
        end_port = int(end_input) if end_input else 1024
    except ValueError:
        print("[-] Ogiltig inport. Använder standardportar 1-1024.")
        start_port, end_port = 1, 1024

    print(f"\n[*] Skannar {target} från port {start_port} till {end_port}...")
    print("[*] Detta kan ta en stund beroende på intervall...\n")

    open_ports = []

    # 2. Använd ThreadPoolExecutor för att köra flera trådar parallellt (gör skanningen mycket snabbare)
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {
            executor.submit(scan_port, target, port): port
            for port in range(start_port, end_port + 1)
        }

        for future in futures:
            port = futures[future]
            try:
                if future.result():
                    print(f"[+] Port {port} är ÖPPEN")
                    open_ports.append(port)
            except Exception:
                pass

    # 3. Sammanfattning
    print("\n-----------------------------------------")
    print(f"Skanning klar! Hittade {len(open_ports)} öppna portar.")
    if open_ports:
        print(f"Öppna portar: {', '.join(map(str, open_ports))}")
    print("-----------------------------------------")


if __name__ == "__main__":
    main()
