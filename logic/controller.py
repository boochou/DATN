#!/usr/bin/env python3
import argparse
import sys
try:
    from .tool_handler import *
except ImportError:
    from tool_handler import *
import os

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
        print(f"Recon found {len(results)} unique subdomains.\n", file=sys.stderr)        
        Utilities.handle_output(output_dir,"reconn",results,d)
        all_results.extend(results)
    return all_results

def check_active_domains(input_file=None, ip_only=False,isCommon=True):
    print(f"Checking active domains from {input_file}, with {ip_only}",file=sys.stderr)
    active_domains={}
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
    if ip_only and ip_only !="false":
        all_results = []
        for d in domains:
            ips = reconn_tool.check_domain_status(d)
            Utilities.handle_output(output_dir,"check_domain",ips,d,True)
            all_results.extend(ips)
            if ips != []:
                active_domains[d] = ips
        print(f"Active domain {len(active_domains)}/{len(domains)}",file=sys.stderr)
        for domain, ips in active_domains.items():
            ip_str = ", ".join(ips)
            sys.stderr.write(f"\n - {ip_str} - \n ")
            sys.stdout.write(f"{domain}\n")
            
        return all_results
    #ip_port collection
    all_results = {}
    for d in domains:
        ips = reconn_tool.ip_port_collect(d,isCommon)
        Utilities.write_to_file(ips,output_dir,"check_domain",d,'json')
        all_results[d] = ips[d]
    return all_results  

def scan_technologies(input_file):
    print(f"Collect technology from {input_file}",file=sys.stderr)
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
    all_results = {}
    #general purpose
    for d in domains: 
        result = reconn_tool.tech_collect_general(d)
        Utilities.write_to_file(result,output_dir,"scan_tech",d,'json')
        all_results[d] = result
        
    # TODO: Implement technology scanning logic
    # if firewall:
    #     print("Finding firewall using Nmap")
    # if os_only:
    #     print("Finding possible OS")
    print(all_results, file=sys.stderr)
    return all_results
    

def collect_resources(input_file,wordlist="None"):
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
    all_results = {}
    for d in domains:
        result = reconn_tool.url_collection(d)
        Utilities.handle_output(output_dir,"url_collection",result,d)
        all_results[d] = list(result)
    return all_results

def configure_tool(limit_rate, update_dict):
    print(f"Setting limit-rate: {limit_rate}")
    print(f"Updating dictionary: {update_dict}")
    # TODO: Implement configuration logic