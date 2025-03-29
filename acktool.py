#!/usr/bin/env python3
import argparse
import sys
def collect_subdomains(input_file, mode):
    print(f"Collecting subdomains in {mode} mode for {input_file}", file=sys.stderr)  # Debug message

    # Fake data for testing (replace with actual logic)
    subdomains = ["sub1.example.com", "sub2.example.com"]

    for sub in subdomains:
        print(sub)  # Output to stdout for piping

def check_active_domains(input_file=None, ip_only=False, port_only=False):
    print(f"Checking active domains from {input_file}")
    if ip_only:
        print("Collecting only IPs")
    elif port_only:
        print("Collecting only Ports")
    # TODO: Implement active domain checking logic
    domains = []
    if input_file:
        with open(input_file, "r") as f:
            domains = f.read().splitlines()
    elif not sys.stdin.isatty():  # If input is piped
        domains = sys.stdin.read().splitlines()
    
    for domain in domains:
        print(f"Active: {domain}")  # Print result for piping

def scan_technologies(firewall, os_only):
    print("Scanning used technologies")
    if firewall:
        print("Finding firewall using Nmap")
    if os_only:
        print("Finding possible OS")
    # TODO: Implement technology scanning logic

def collect_resources():
    print("Collecting URL and directory resources")
    # TODO: Implement resource collection logic

def configure_tool(limit_rate, update_dict):
    print(f"Setting limit-rate: {limit_rate}")
    print(f"Updating dictionary: {update_dict}")
    # TODO: Implement configuration logic
def print_logo():
    logo = """
     █████╗  ██████╗██╗  ██╗    ████████╗ ██████╗  ██████╗ ██╗     
    ██╔══██╗██╔════╝██║██║      ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
    ███████║██║     ███║           ██║   ██║   ██║██║   ██║██║     
    ██╔══██║██║     ██║██║         ██║   ██║   ██║██║   ██║██║     
    ██║  ██║╚██████╗██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗
    ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
    """
    print(logo)
    
def main():
    if sys.stdout.isatty():
        print_logo()
    parser = argparse.ArgumentParser(description="Recon Tool with AI Agent")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    subdomains_parser = subparsers.add_parser("subdomains", help="Collect subdomains")
    subdomains_parser.add_argument("input_file", help="File or domain/URL to scan")
    subdomains_parser.add_argument("--mode", choices=["active", "passive"], default="passive", help="Choose scanning mode")
    
    domain_parser = subparsers.add_parser("check_domain", help="Check active domains")
    domain_parser.add_argument("input_file", nargs="?", help="File or domain list (or pipe input)")
    domain_parser.add_argument("--ip-only", action="store_true", help="Only collect IPs")
    domain_parser.add_argument("--port-only", action="store_true", help="Only collect Ports")
    
    tech_parser = subparsers.add_parser("scan_tech", help="Scan used technologies in general")
    tech_parser.add_argument("--firewall", action="store_true", help="Find firewall using Nmap")
    tech_parser.add_argument("--os", action="store_true", help="Find all possible OS")
    
    resource_parser = subparsers.add_parser("collect_resources", help="Collect URL and directory resources")
    
    config_parser = subparsers.add_parser("config", help="Configuration for limit-rate and dictionary")
    config_parser.add_argument("limit_rate", help="Set limit-rate for brute-force")
    config_parser.add_argument("update_dict", help="Update dictionary")
    
    args = parser.parse_args()
    
    if args.command == "subdomains":
        collect_subdomains(args.input_file, args.mode)
    elif args.command == "check_domain":
        check_active_domains(args.input_file, args.ip_only, args.port_only)
    elif args.command == "scan_tech":
        scan_technologies(args.firewall, args.os)
    elif args.command == "collect_resources":
        collect_resources()
    elif args.command == "config":
        configure_tool(args.limit_rate, args.update_dict)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
