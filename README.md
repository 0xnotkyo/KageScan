<div align="center">

  <img src="https://raw.githubusercontent.com/0xnotkyo/KageScan/main/assets/logo.png" height="128">

<h2 align="center">KageScan - Network Scanner</h2>

<p align="center"><a href="https://github.com/0xnotkyo/twt/blob/main/LICENSE"><img src="https://img.shields.io/static/v1?style=for-the-badge&label=LICENSE&message=MIT&colorA=000000&colorB=ff0000"/></a></p>

<img src="https://raw.githubusercontent.com/0xnotkyo/KageScan/main/assets/bar.png">

</div>

## 🎏 About  

  A network scanning tool similar to `nmap` with port scanning and directory enumeration features. Built with **Python**.


## ⛩️ Features
- **Fast TCP Port Scanning** — Multi-threaded scanning for high perfomance
- **Service Detection** — Automatically identifies services running on open ports
- **Directory Enumeration** — Finds hidden web directories using custom wordlists or gobuster
- **JSON Export** — Easily save and parse scan results
- **Clipboard Integration** — Quickly copy open ports to your clipboard with a single flag

---

## ⚙️ Installation

It is recommended to use a virtual environment to manage dependencies:

```bash
# Create the virtual environment
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📦 Optional Dependencies

For enhanced functionality, you may install these tools:

```bash
# For directory scanning (optional)
sudo apt install gobuster

# For clipboard support (-c flag)
sudo apt install xclip
```
---

## 🎋 Usage 

### Basic scan
```bash
python3 main.py 192.168.1.1
```

### Scan specific ports
```bash
python3 main.py 192.168.1.1 -p 80,443
python3 main.py 192.168.1.1 -p 1-1000
```

### With service detection
```bash
python3 main.py 192.168.1.1 --service-detection
```

### With service detection
```bash
# Manual mode
python3 main.py 192.168.1.1 --directory-scan

# Using gobuster
python3 main.py 192.168.1.1 --directory-scan --gobuster
```

### Copy open ports to clipboard
```bash
python3 main.py 192.168.1.1 -c
```

### Save results
```bash
python3 main.py 192.168.1.1 -o results.json
```
---

## 🦥 Options

| Flag | Description |
| --- | --- 
| `-p, --ports` | Ports range (e.g., 21,22,80,443) | 
| `-t, --threads` | Number of threads (def: 100)
| `-o --output` | Save results to JSON file
| `--directory-scan` | Enable directory enumeration
| `--gobuster` | Use gobuster for enumeration
| `w, -wordlist` | Wordlist file for enumeration
| `--timeout` | Connection timeout
| `-s, --service-detection` | Enable service detection
| `-c, --copy` | Copy open ports to clipboard (requires xclip)

---

## 🏯 Example Output

<div align="center">

  <img src="https://raw.githubusercontent.com/0xnotkyo/KageScan/main/assets/output_example.png">

---

<div align="center">

**Made with ♥ by [0xnotkyo](https://github.com/0xnotkyo)** 

</div>
