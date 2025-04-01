#!/usr/bin/env python3
import argparse
import sys
from logic import *

output_dir = "results"
def collect_subdomains(input_value, mode,w):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Collecting subdomains for {input_value}", file=sys.stderr)
    if not sys.stdin.isatty():  # If input is piped
        domains = sys.stdin.read().splitlines()
    else:
        try:
            domains = Utilities.check_input(input_value)['domain']
        except Exception as e:
            raise InvalidInputError(f"Error processing input: {str(e)}") from e
    reconn_tool = Reconn()
    all_results = []
    for d in domains:
        with ThreadPoolExecutor() as executor:
                passive_future = executor.submit(reconn_tool.passive_recon, d)
                active_future = ''
                if mode:
                    args = (d, w) if w else (d,)
                    active_future = executor.submit(reconn_tool.active_recon, *args)
                passive_results = passive_future.result()
                active_results = active_future.result() if active_future else []
        print(f"Passive recon found {len(passive_results)} unique subdomains.\n", file=sys.stderr)       
        print(f"Active recon found {len(active_results)} unique subdomains.\n", file=sys.stderr)       
        results = sorted(set(passive_results).union(active_results))  
        print(f"Active recon found {len(results)} unique subdomains.\n", file=sys.stderr)        
        Utilities.handle_output(output_dir,"reconn",results,d)
        all_results.extend(results)
    return all_results

def check_active_domains(input_file=None, ip_only=False,isCommon=True):
    print(f"Checking active domains from {input_file}",file=sys.stderr)
    domains = []
    #handle input
    if input_file:
        try:
            with open(input_file, "r") as f:
                domains = f.read().splitlines()
        except:
            domains = [input_file] if Utilities.is_valid_domain(input_file) else []
    elif not sys.stdin.isatty():  # If input is piped
        domains = sys.stdin.read().splitlines()
    reconn_tool = Reconn()
    #ip_only option
    if ip_only:
        all_results = []
        for d in domains:
            ips = reconn_tool.ip_only(d)
            Utilities.handle_output(output_dir,"check_domain",ips,d)
            all_results.extend(ips)
        return all_results
    #ip_port collection
    all_results = []
    for d in domains:
        print("Checking", d)
        ips = reconn_tool.ip_port_collect(d,isCommon)
        Utilities.write_to_file(ips,output_dir,"check_domain",d)
        # all_results.extend(ips)
    return all_results
    
    

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
    
    domain_parser = subparsers.add_parser("check_domain", help="Check active domains")
    domain_parser.add_argument("input", nargs="?", help="File or domain list (or pipe input)")
    domain_parser.add_argument("--ip-only", action="store_true", help="Only collect IPs")
    domain_parser.add_argument("--all-port", action="store_true", help="Only collect IPs")
    
    tech_parser = subparsers.add_parser("scan_tech", help="Scan used technologies in general")
    tech_parser.add_argument("--firewall", action="store_true", help="Find firewall using Nmap")
    tech_parser.add_argument("--os", action="store_true", help="Find all possible OS")
    
    resource_parser = subparsers.add_parser("collect_resources", help="Collect URL and directory resources")
    
    config_parser = subparsers.add_parser("config", help="Configuration for limit-rate and dictionary")
    config_parser.add_argument("limit_rate", help="Set limit-rate for brute-force")
    config_parser.add_argument("update_dict", help="Update dictionary")
    
    args = parser.parse_args()
    
    if args.command == "subdomains":
        if args.wordlist and not args.active:
            parser.error("The -w option requires -a to be specified.")
        collect_subdomains(args.input, args.active,args.wordlist)
    elif args.command == "check_domain":
        if args.ip_only and args.all_port:
            parser.error("Can not scan port when just collecting IP option")
        check_active_domains(args.input, args.ip_only,not args.all_port)
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
