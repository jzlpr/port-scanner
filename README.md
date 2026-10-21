# 🔍 port-scanner

> 🎯 A lightweight Python network port scanner that wraps the power of **Nmap** through the **nmapthon2** library - discover live hosts, open TCP ports, and running services in seconds.

---

## 📜 Badges
![Python](https://img.shields.io/badge/Powered%20by-Python-aa82B4?style=for-the-badge&logo=nmap&logoColor=white)
![Nmap](https://img.shields.io/badge/Powered%20by-Nmap-4682B4?style=for-the-badge&logo=nmap&logoColor=white)
![Library](https://img.shields.io/badge/Library-nmapthon2-00B4D8?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Shell](https://img.shields.io/badge/Interface-CLI-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

---

## ✨ Features

- 🖥️ **Interactive CLI** - prompts for a target IP/hostname and a port range with sensible defaults
- ⚡ **Nmap-powered scanning** - uses Nmap's `-T4` (aggressive) timing template for fast results
- 🌐 **Multi-host discovery** - iterates every host found on the target network
- 🏷️ **Hostname resolution** - displays reverse-DNS hostnames when available
- 🔓 **Open-port reporting** - clean aligned table of `PORT / STATE / SERVICE` for every open TCP port
- 🛡️ **Robust error handling** - defensive attribute access and graceful fallbacks; errors go to `stderr`
- 🧩 **Version-tolerant** - compatible with multiple nmapthon2 API styles (objects or dicts)

---

## 📋 Requirements

| Requirement | 📦 Details |
|-------------|------------|
| 🐍 Python | 3.6 or newer |
| 🗺️ Nmap | The `nmap` binary must be installed and on your `PATH` |
| 📚 nmapthon2 | Python wrapper library (`pip install nmapthon2`) |

<details>
<summary>🛠️ Install Nmap on your system</summary>

```bash
# 🐧 Debian / Ubuntu
sudo apt install nmap

# 🍎 macOS (Homebrew)
brew install nmap

# 🪟 Windows
# Download the installer from https://nmap.org/download.html
```
</details>

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone --depth 1 https://github.com/jzlpr/port-scanner.git
cd port-scanner
```

### 2️⃣ Create a virtual environment 💻

```bash
python3 -m venv .venv
source .venv/bin/activate      # 🐧 Linux / 🍎 macOS
# .venv\Scripts\activate       # 🪟 Windows
```

### 3️⃣ Install dependencies 📦

```bash
pip install nmapthon2
```

### 4️⃣ Run the scanner ▶️

```bash
python port-scanner3.py
```

### 💬 Example session

```text
[*] Initializing Nmap scan against target: 192.168.1.1 (Ports: 1-1024)
[+] Scan completed successfully.

Host: 192.168.1.1 (router.local) - Status: up

    PORT    STATE   SERVICE
    ----    -----   -------
    80/tcp  open    http
    443/tcp open    https
```

---

### 🔬 Code walkthrough

| 🧩 Block | 📝 What it does |
|----------|-----------------|
| 📥 `import sys` | Provides access to `stderr` for error reporting |
| 📚 `import nmapthon2 as nm2` | Loads the Nmap wrapper library under the alias `nm2` |
| ⚙️ `run_port_scanner(target_ip, ports)` | Main routine - orchestrates the whole scan |
| 🖨️ `print("[*] Initializing ...")` | Status banner showing target and port range |
| 🏗️ `nm2.NmapScanner()` | Instantiates the reusable scanner object that shells out to `nmap` |
| 📡 `scanner.scan(targets=..., ports=..., arguments="-T4")` | Executes the actual Nmap scan and returns an iterable of `Host` objects |
| 🚧 `if not result:` | Early-exit guard when the scan yields nothing |
| 🔁 `for host in result:` | Iterates every machine discovered by Nmap |
| 🌐 `getattr(host, "ipv4", ...)` | Safely extracts the host IP with layered fallbacks |
| 🏷️ `host.hostnames()` | Retrieves reverse-DNS hostnames inside a defensive `try/except` |
| 📊 `host_state` | Reads the host up/down state (defaults to `"up"`) |
| 🔌 `host.tcp_ports` | Fetches the TCP port container (method or list, depending on API version) |
| 🧾 `for port in ports_found:` | Iterates each `Port` object (`number`, `state`, `service`) |
| 🔓 `if p_state == "open":` | Filters the report down to open ports only |
| ❌ `except Exception as e:` | Catches any scan failure and logs it to `stderr` |
| 🎬 `if __name__ == "__main__":` | Entry-point guard - only runs when executed directly |
| 💬 `input(...)` calls | Interactive prompts with `192.168.1.1` and `1-1024` defaults |

---

## 📂 Project Structure

```text
port-scanner/
├── 🐍 port-scanner.py    # ⭐ Main scanner script
├── 📁 iterations/         # 🗂️ Earlier versions kept for history
│   ├── 🐍 port-scanner.py
│   ├── 🐍 port-scanner2.py
│   ├── 🐍 main.py
│   ├── 🐍 gemini-ps.py
│   ├── 🐍 widd-portscanner.py
│   └── 🔧 diagnose_script.py
├── 📄 README.md           # 📖 This documentation
└── 🙈 .gitignore          # 🚫 Files excluded from version control
```

---

## ⚙️ Command-Line Behavior

| 🎛️ Prompt | 🔑 Default | 📝 Accepted format |
|-----------|-----------|--------------------|
| 🎯 Target IP / hostname | `192.168.1.1` | `10.0.0.5`, `scanme.nmap.org`, CIDR like `192.168.1.0/24` |
| 🔌 Port range | `1-1024` | `1-65535`, `80,443,8080`, or a single port like `22` |

---

## ⚠️ Legal & Ethical Notice

> 🚨 **Only scan systems you own or have explicit written permission to test.**
> Unauthorized port scanning may be illegal in your jurisdiction and violates most
> acceptable-use policies. Use this tool for 🔐 education, 🛠️ administration of your
> own network, or sanctioned penetration-testing engagements only.

---

## 🗺️ Roadmap

- [x] 🎯 Basic host & TCP port discovery
- [x] 🏷️ Hostname resolution
- [ ] 🖥️ UDP port scanning support
- [ ] 📤 Export results to JSON / CSV
- [ ] 🎨 Colorized terminal output
- [ ] 🧵 Concurrent scanning of multiple targets

---

## 🤝 Contributing

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. ✍️ Commit your changes (`git commit -m "Add amazing feature"`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔃 Open a Pull Request

---

<div align="center">

Made with ❤️ and 🐍 Python - powered by ⚡ [Nmap](https://nmap.org)

⭐ Star this repo if you found it useful!

</div>
