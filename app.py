#!/usr/bin/env python3
"""
NetScope Web Dashboard
Repository: github.com/frangelbarrera/python-subnet-calculator
License: MIT
"""

import ipaddress
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# ─── Core Calculation Logic (shared with CLI) ─────────────────────────────────

def _get_ip_class(ip: ipaddress.IPv4Address) -> str:
    first_octet = int(str(ip).split(".")[0])
    if first_octet < 128:
        return "A"
    elif first_octet < 192:
        return "B"
    elif first_octet < 224:
        return "C"
    elif first_octet < 240:
        return "D (Multicast)"
    return "E (Reserved)"


def calculate_subnet(cidr: str) -> dict:
    """
    Parse a CIDR string and return a dict with all subnet attributes.

    Raises:
        ValueError: If the input is not valid CIDR notation.
    """
    try:
        network = ipaddress.IPv4Network(cidr.strip(), strict=False)
    except ValueError as exc:
        raise ValueError(f"Invalid CIDR notation: '{cidr}'") from exc

    hosts = list(network.hosts())

    return {
        "cidr":            str(network),
        "network_addr":    str(network.network_address),
        "broadcast_addr":  str(network.broadcast_address),
        "subnet_mask":     str(network.netmask),
        "wildcard_mask":   str(network.hostmask),
        "prefix_length":   network.prefixlen,
        "ip_version":      network.version,
        "total_addresses": network.num_addresses,
        "usable_hosts":    len(hosts),
        "first_host":      str(hosts[0])  if hosts else "N/A",
        "last_host":       str(hosts[-1]) if hosts else "N/A",
        "ip_class":        _get_ip_class(network.network_address),
        "is_private":      network.is_private,
        "is_loopback":     network.is_loopback,
        "is_multicast":    network.is_multicast,
        "supernet":        str(network.supernet()),
    }


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/calculate", methods=["POST"])
def api_calculate():
    data = request.get_json(silent=True) or {}
    cidr = data.get("cidr", "").strip()

    if not cidr:
        return jsonify({"error": "No CIDR address provided."}), 400

    try:
        result = calculate_subnet(cidr)
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 422


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
