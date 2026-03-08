#!/usr/bin/env python3
"""
NetScope - Professional Subnet Intelligence Tool
Repository: github.com/frangelbarrera/python-subnet-calculator
License: MIT
"""

import ipaddress
import sys
import argparse
from typing import Optional


# ─── ANSI Color Palette ───────────────────────────────────────────────────────

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    # Foregrounds
    WHITE   = "\033[97m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    GRAY    = "\033[90m"

    # Backgrounds
    BG_DARK = "\033[48;5;234m"


# ─── Banner ───────────────────────────────────────────────────────────────────

BANNER = f"""
{C.CYAN}{C.BOLD}
 ███╗   ██╗███████╗████████╗███████╗ ██████╗ ██████╗ ██████╗ ███████╗
 ████╗  ██║██╔════╝╚══██╔══╝██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝
 ██╔██╗ ██║█████╗     ██║   ███████╗██║     ██║   ██║██████╔╝█████╗
 ██║╚██╗██║██╔══╝     ██║   ╚════██║██║     ██║   ██║██╔═══╝ ██╔══╝
 ██║ ╚████║███████╗   ██║   ███████║╚██████╗╚██████╔╝██║     ███████╗
 ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚══════╝
{C.RESET}{C.GRAY}  Professional Subnet Intelligence Tool  ·  v1.0.0{C.RESET}
"""


# ─── Core Calculation Logic ───────────────────────────────────────────────────

def calculate_subnet(cidr: str) -> dict:
    """
    Parse a CIDR string and return a dict with all subnet attributes.

    Args:
        cidr: Network address in CIDR notation (e.g. '192.168.1.0/24').

    Returns:
        Dictionary containing all computed subnet fields.

    Raises:
        ValueError: If the CIDR string is invalid.
    """
    try:
        network = ipaddress.IPv4Network(cidr, strict=False)
    except ValueError as exc:
        raise ValueError(f"Invalid CIDR notation: '{cidr}'") from exc

    hosts = list(network.hosts())
    num_hosts = len(hosts)

    return {
        "cidr":           str(network),
        "network_addr":   str(network.network_address),
        "broadcast_addr": str(network.broadcast_address),
        "subnet_mask":    str(network.netmask),
        "wildcard_mask":  str(network.hostmask),
        "prefix_length":  network.prefixlen,
        "ip_version":     network.version,
        "total_addresses":network.num_addresses,
        "usable_hosts":   num_hosts,
        "first_host":     str(hosts[0])  if hosts else "N/A",
        "last_host":      str(hosts[-1]) if hosts else "N/A",
        "host_range":     (
            f"{hosts[0]}  →  {hosts[-1]}" if hosts else "No usable hosts"
        ),
        "ip_class":       _get_ip_class(network.network_address),
        "is_private":     network.is_private,
        "is_loopback":    network.is_loopback,
        "is_multicast":   network.is_multicast,
        "supernet":       str(network.supernet()),
    }


def _get_ip_class(ip: ipaddress.IPv4Address) -> str:
    """Return the classful class (A/B/C/D/E) of an IPv4 address."""
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


# ─── Display Layer ────────────────────────────────────────────────────────────

def _separator(width: int = 56, char: str = "─") -> str:
    return f"{C.GRAY}{char * width}{C.RESET}"


def _field(label: str, value: str, accent: str = C.GREEN) -> str:
    label_fmt = f"{C.GRAY}{label:<22}{C.RESET}"
    value_fmt = f"{accent}{C.BOLD}{value}{C.RESET}"
    return f"  {label_fmt}{value_fmt}"


def _flag(label: str, state: bool) -> str:
    icon  = f"{C.GREEN}✔{C.RESET}" if state else f"{C.RED}✘{C.RESET}"
    label_fmt = f"{C.GRAY}{label:<22}{C.RESET}"
    return f"  {label_fmt}{icon}"


def render_result(data: dict) -> None:
    """Pretty-print the subnet calculation result to stdout."""
    print()
    print(_separator(56, "═"))
    print(f"{C.CYAN}{C.BOLD}  SUBNET ANALYSIS  ·  {data['cidr']}{C.RESET}")
    print(_separator(56, "═"))

    # ── Network Identity ──
    print(f"\n{C.YELLOW}{C.BOLD}  [ Network Identity ]{C.RESET}")
    print(_separator())
    print(_field("CIDR Notation",    data["cidr"],           C.CYAN))
    print(_field("Network Address",  data["network_addr"],   C.WHITE))
    print(_field("Subnet Mask",      data["subnet_mask"],    C.WHITE))
    print(_field("Wildcard Mask",    data["wildcard_mask"],  C.WHITE))
    print(_field("Broadcast Address",data["broadcast_addr"], C.MAGENTA))
    print(_field("Prefix Length",    f"/{data['prefix_length']}", C.WHITE))
    print(_field("IP Class",         data["ip_class"],       C.WHITE))

    # ── Host Range ──
    print(f"\n{C.YELLOW}{C.BOLD}  [ Host Range ]{C.RESET}")
    print(_separator())
    print(_field("First Usable Host", data["first_host"],     C.GREEN))
    print(_field("Last Usable Host",  data["last_host"],      C.GREEN))
    print(_field("Host Range",        data["host_range"],     C.GREEN))
    print(_field("Usable Hosts",
                 f"{data['usable_hosts']:,}", C.GREEN))
    print(_field("Total Addresses",
                 f"{data['total_addresses']:,}", C.WHITE))

    # ── Network Flags ──
    print(f"\n{C.YELLOW}{C.BOLD}  [ Network Flags ]{C.RESET}")
    print(_separator())
    _flag_line("Private Range",  data["is_private"])
    _flag_line("Loopback",       data["is_loopback"])
    _flag_line("Multicast",      data["is_multicast"])

    # ── Extra ──
    print(f"\n{C.YELLOW}{C.BOLD}  [ Additional Info ]{C.RESET}")
    print(_separator())
    print(_field("IP Version",    f"IPv{data['ip_version']}", C.BLUE))
    print(_field("Supernet",      data["supernet"],           C.BLUE))

    print()
    print(_separator(56, "═"))
    print()


def _flag_line(label: str, state: bool) -> None:
    icon  = f"{C.GREEN}● Private{C.RESET}" if state else f"{C.RED}● Public{C.RESET}"
    if label == "Loopback":
        icon = f"{C.GREEN}● Yes{C.RESET}" if state else f"{C.GRAY}● No{C.RESET}"
    if label == "Multicast":
        icon = f"{C.MAGENTA}● Yes{C.RESET}" if state else f"{C.GRAY}● No{C.RESET}"
    label_fmt = f"{C.GRAY}{label:<22}{C.RESET}"
    print(f"  {label_fmt}{icon}")


def render_error(message: str) -> None:
    """Print a styled error message to stderr."""
    print(f"\n  {C.RED}{C.BOLD}[ERROR]{C.RESET}  {C.WHITE}{message}{C.RESET}\n",
          file=sys.stderr)


# ─── Interactive Mode ─────────────────────────────────────────────────────────

def interactive_mode() -> None:
    """Run an interactive REPL loop for continuous subnet queries."""
    print(BANNER)
    print(f"  {C.GRAY}Enter a network in CIDR notation. Type {C.RESET}"
          f"{C.CYAN}'exit'{C.RESET}{C.GRAY} or {C.RESET}"
          f"{C.CYAN}'q'{C.RESET}{C.GRAY} to quit.{C.RESET}\n")

    while True:
        try:
            raw = input(f"  {C.CYAN}netscope{C.RESET}{C.GRAY}>{C.RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n  {C.GRAY}Goodbye.{C.RESET}\n")
            sys.exit(0)

        if not raw:
            continue
        if raw.lower() in {"exit", "quit", "q"}:
            print(f"\n  {C.GRAY}Goodbye.{C.RESET}\n")
            sys.exit(0)

        try:
            data = calculate_subnet(raw)
            render_result(data)
        except ValueError as exc:
            render_error(str(exc))


# ─── CLI Argument Mode ────────────────────────────────────────────────────────

def parse_args() -> Optional[argparse.Namespace]:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="netscope",
        description="NetScope – Professional Subnet Intelligence Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python subnet_calc.py 192.168.1.0/24\n"
            "  python subnet_calc.py 10.0.0.0/8\n"
            "  python subnet_calc.py              # interactive mode\n"
            "\n"
            "Repository: https://github.com/frangelbarrera/python-subnet-calculator\n"
        ),
    )
    parser.add_argument(
        "cidr",
        nargs="?",
        metavar="CIDR",
        help="Network address in CIDR notation (e.g. 192.168.1.0/24)",
    )
    return parser.parse_args()


# ─── Entry Point ──────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()

    if args.cidr:
        # Single-shot mode
        print(BANNER)
        try:
            data = calculate_subnet(args.cidr)
            render_result(data)
        except ValueError as exc:
            render_error(str(exc))
            sys.exit(1)
    else:
        # Interactive REPL
        interactive_mode()


if __name__ == "__main__":
    main()
