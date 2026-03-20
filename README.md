# Professional Subnet Intelligence Tool

> A precision-built subnet calculator for network engineers and security professionals.  
> Zero dependencies · Pure Python · CIDR-aware · Battle-tested output.

```

---

## ✦ Features

| Feature | Description |
|---|---|
| **CIDR Parsing** | Full support for IPv4 CIDR notation (`/0` → `/32`) |
| **Subnet Mask** | Computes dotted-decimal netmask and wildcard mask |
| **Network & Broadcast** | Identifies network and broadcast addresses precisely |
| **Usable Host Range** | First and last usable IP, total count |
| **IP Classification** | Class A / B / C / D / E detection |
| **Network Flags** | Private, loopback, and multicast detection |
| **Supernet** | Computes the immediate supernet |
| **Error Handling** | Validates input with clear, actionable error messages |
| **CLI REPL** | Interactive loop mode for rapid multi-network analysis |
| **Web Dashboard** | Dark-mode Flask UI with KPI cards, prefix visualizer, flags |
| **JSON API** | `POST /api/calculate` endpoint for programmatic use |
| **Zero stdlib deps** | CLI uses only Python's built-in `ipaddress` module |

---

## Quick Start

### Requirements

- Python 3.7+
- Flask (web dashboard only)

### Installation

```bash
git clone https://github.com/frangelbarrera/python-subnet-calculator.git
cd python-subnet-calculator
pip install -r requirements.txt
```

---

## CLI Usage

**Single network (one-shot mode):**

```bash
python subnet_calc.py 192.168.1.0/24
```

**Interactive REPL mode:**

```bash
python subnet_calc.py
```

```
netscope> 10.0.0.0/8
netscope> 172.16.0.0/12
netscope> exit
```

---

## Web Dashboard

Start the Flask server:

```bash
python app.py
```

Then open your browser at: **http://localhost:5000**

The dashboard provides:
- **KPI strip** — prefix length, usable hosts, total addresses, IP class
- **Network Identity card** — network/broadcast/mask/wildcard/supernet
- **Host Range card** — first/last usable host with counters
- **Prefix Utilization bar** — visual representation of the `/prefix` within `/0`→`/32`
- **Network Flags** — Private / Loopback / Multicast indicators
- **Mask Breakdown** — network bits vs host bits
- **Copy JSON** — exports full result as JSON to clipboard

### REST API

```bash
curl -X POST http://localhost:5000/api/calculate \
     -H "Content-Type: application/json" \
     -d '{"cidr": "192.168.1.0/24"}'
```

---

## Example Output

```
══════════════════════════════════════════════════════
  SUBNET ANALYSIS  ·  192.168.1.0/24
══════════════════════════════════════════════════════

  [ Network Identity ]
  ────────────────────────────────────────────────────
  CIDR Notation         192.168.1.0/24
  Network Address       192.168.1.0
  Subnet Mask           255.255.255.0
  Wildcard Mask         0.0.0.255
  Broadcast Address     192.168.1.255
  Prefix Length         /24
  IP Class              C

  [ Host Range ]
  ────────────────────────────────────────────────────
  First Usable Host     192.168.1.1
  Last Usable Host      192.168.1.254
  Host Range            192.168.1.1  →  192.168.1.254
  Usable Hosts          254
  Total Addresses       256

  [ Network Flags ]
  ────────────────────────────────────────────────────
  Private Range         ● Private
  Loopback              ● No
  Multicast             ● No

  [ Additional Info ]
  ────────────────────────────────────────────────────
  IP Version            IPv4
  Supernet              192.168.0.0/23

══════════════════════════════════════════════════════
```

---

## Project Structure

```
python-subnet-calculator/
├── subnet_calc.py        # CLI tool — all logic and terminal interface
├── app.py                # Flask web server + REST API
├── templates/
│   └── index.html        # Web dashboard (single-file, dark mode)
├── requirements.txt      # Dependencies (Flask for web mode)
└── README.md             # This file
```

---

## Roadmap

- [x] CLI tool with ANSI color output
- [x] Interactive REPL mode
- [x] Web dashboard (dark mode)
- [x] REST JSON API
- [ ] IPv6 support
- [ ] VLSM (Variable Length Subnet Masking) calculator
- [ ] Subnet split / summarization
- [ ] CSV / export flag (`--csv`)

---
