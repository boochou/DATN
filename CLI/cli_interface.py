#!/usr/bin/env python3
import argparse
import sys
from logic.controller import *
def print_logo():
    logo = """
     █████╗  ██████╗██╗   ██╗   ████████╗ ██████╗  ██████╗ ██╗     
    ██╔══██╗██╔════╝██║ ██║     ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
    ███████║██║     ████║          ██║   ██║   ██║██║   ██║██║     
    ██╔══██║██║     ██║ ██║        ██║   ██║   ██║██║   ██║██║     
    ██║  ██║╚██████╗██║   ██║      ██║   ╚██████╔╝╚██████╔╝███████╗
    ╚═╝  ╚═╝ ╚═════╝╚═╝   ╚═╝      ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
    """
    print(logo)
    
def main():
    if sys.stdout.isatty():
        print_logo()
    parser = argparse.ArgumentParser(description="Recon Tool with AI Agent")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    subdomains_parser = subparsers.add_parser("subdomains", help="Collect subdomains")
    subdomains_parser.add_argument("input", nargs="?",help="File or domain/URL to scan")
    subdomains_parser.add_argument("-a", "--active", action="store_true", help="Active scanning")
    subdomains_parser.add_argument("-w","--wordlist", type=str, help="Wordlist for scanning")
    
    domain_parser = subparsers.add_parser("ip_port", help="Collect IP/Port - scans the most common 1,000 ports as default ")
    domain_parser.add_argument("input", nargs="?", help="File or domain list (or pipe input)")
    domain_parser.add_argument("--ip-only", action="store_true", help="Only collect IPs")
    domain_parser.add_argument("--all-port", action="store_true", help="Scan all port (from 1 through 65535)")
    
    tech_parser = subparsers.add_parser("scan_tech", help="Scan used technologies in general")
    tech_parser.add_argument("input", nargs="?", help="File or domain list (or pipe input)")
    # tech_parser.add_argument("--firewall", action="store_true", help="Find firewall using Nmap")
    # tech_parser.add_argument("--os", action="store_true", help="Find all possible OS")
    
    resource_parser = subparsers.add_parser("collect_resources", help="Collect URL and directory resources")
    resource_parser.add_argument("input", nargs="?", help="File or domain list (or pipe input)")
    resource_parser.add_argument("-w","--wordlist", type=str, help="Wordlist for scanning")
    
    # config_parser = subparsers.add_parser("config", help="Configuration for limit-rate and dictionary")
    # config_parser.add_argument("limit_rate", help="Set limit-rate for brute-force")
    # config_parser.add_argument("update_dict", help="Update dictionary")
    
    args = parser.parse_args()
    
    if args.command == "subdomains":
        if args.wordlist and not args.active:
            parser.error("The -w option requires -a to be specified.")
        collect_subdomains(args.input, args.active,args.wordlist)
    elif args.command == "ip_port":
        if args.ip_only and args.all_port:
            parser.error("Can not scan port when just collecting IP option")
        check_active_domains(args.input, args.ip_only,not args.all_port)
    elif args.command == "scan_tech":
        scan_technologies(args.input)
    elif args.command == "collect_resources":
        collect_resources(args.input,args.wordlist)
    # elif args.command == "config":
    #     configure_tool(args.limit_rate, args.update_dict)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
