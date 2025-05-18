import json
import os
import re
import sys
import subprocess
from knock import KNOCKPY
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import socket
import whois
RED = "\033[91m"
RESET = "\033[0m"  # Reset về màu mặc định
class InvalidInputError(Exception):
    """Custom exception for invalid input values."""
    pass
class Utilities:
    @staticmethod
    def extract_result(output, domain):
        match = re.search(rf"{re.escape(domain)}\s*\[(.*?)\]", output)
        return match.group(1) if match else None
    @staticmethod
    def fuzzify_url(url):
        pattern = r'(?<==)([^&#/?]+)'  # Tìm giá trị ngay sau dấu '=' và trước ký tự đặc biệt
        fuzzed_url = re.sub(pattern, 'FUZZ', url)
        return fuzzed_url
    @staticmethod
    def remove_ansi_codes(text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
    @staticmethod
    def handle_output(output_dir,type,results,d,hidden =False):  
        subfolder_path = os.path.join(output_dir, type)
        os.makedirs(subfolder_path, exist_ok=True)
        output_file = os.path.join(subfolder_path, f"{d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        print(f"Writing results for {d} to {output_file}",file=sys.stderr)
        with open(output_file, "w") as file:
            file.write("\n".join(results))
        if hidden:  
            print("\n".join(results),file=sys.stderr)
        else: print("\n".join(results))
    @staticmethod
    def is_valid_domain(domain: str) -> bool:
        pattern = re.compile(r'^(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,}$')
        return bool(pattern.match(domain))

    @staticmethod
    def check_input(input_value: str) -> dict:   
        if os.path.isfile(input_value):
            domains = []
            with open(input_value, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if Utilities.is_valid_domain(line):
                        domains.append(line)
            return {"domain": domains}
        elif Utilities.is_valid_domain(input_value):
            return {"domain": [input_value]}
        else:
            raise InvalidInputError("Not a domain or a valid file path.")

    @staticmethod
    def write_to_file(data: dict, output_dir,type,d,file_type='txt'):
        subfolder_path = os.path.join(output_dir, type)
        os.makedirs(subfolder_path, exist_ok=True)
        output_file = os.path.join(subfolder_path, f"{d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_type}")
        print(f"Writing results for {d} to {output_file}",file=sys.stderr)
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4,ensure_ascii=False)

    @staticmethod
    def parse_nmap_output(nmap_output):
        result = {}
        
        # Split the output into sections for each scan report
        reports = nmap_output.strip().split("Nmap scan report for ")
        
        for report in reports[1:]:  # Skip the first empty entry
            lines = report.split("\n")
            domain_info = lines[0].strip()
            domain_match = re.match(r"(.*?) \((.*?)\)", domain_info)
            
            if domain_match:
                domain, scanned_ip = domain_match.groups()
            else:
                continue  # Skip if format is unexpected

            result.setdefault(domain, {"scanned_ips": [], "additional_ips": [], "rDNS": {}, "ports": []})
            result[domain]["scanned_ips"].append(scanned_ip)
            
            for line in lines:
                line = line.strip()
                
                if line.startswith("Other addresses for"):
                    line = re.sub(r".*not scanned\):\s*", "", line)
                    ips = re.findall(r"\d+\.\d+\.\d+\.\d+|[\da-fA-F:]+", line)
                    result[domain]["additional_ips"].extend(ips)
                    
                elif line.startswith("rDNS record for"):
                    match = re.match(r"rDNS record for ([\d\.]+):\s(.+)", line)
                    if match:
                        ip, rdns = match.groups()
                        result[domain]["rDNS"][ip] = rdns
                        
                elif re.match(r"\d+/tcp", line):
                    match = re.match(r"(\d+)/tcp\s+(\w+)\s+(\S+)(?:\s+(.*))?", line)
                    if match:
                        port, state, service, version = match.groups()
                        result[domain]["ports"].append({
                            "port": int(port),
                            "state": state,
                            "service": service,
                            "version": version if version else ""
                        })
        return result 
    @staticmethod
    def run_binary(binary_name, arguments,domain=None):
        try:
            result = subprocess.run([binary_name] + arguments, check=True, text=True, capture_output=True)
            if binary_name != 'paramspider':
                output = result.stdout.strip().splitlines() 
            else:   
                result_file = f"./results/{domain}.txt"
                output=[]
                if os.path.exists(result_file):
                    with open(result_file, "r") as file:
                        output = [line.strip() for line in file.readlines() if line.strip()]
                os.remove(result_file)
            # print(f"{binary_name} found {len(output)} results.", file=sys.stderr)           
            return binary_name, output
        except subprocess.CalledProcessError as e:
            print(f"Error running {binary_name}: {e.stderr}", file=sys.stderr)
            return binary_name, []
        except FileNotFoundError:
            print(f"Error: The binary '{binary_name}' was not found. Make sure it is installed and in your PATH.", file=sys.stderr)
            return binary_name, []
class Reconn:
    def __init__(self):
        self.binaries = {
            "subfinder": lambda domain: ["-d", domain],
            "assetfinder": lambda domain: [domain]
        }
        self.urltools = {
            "paramspider": lambda domain: ["-d", domain],
            "katana": lambda domain: ["-u", domain]
        }
        self.techtools = {
            "/usr/bin/httpx": lambda domain: ["-u", domain]
        }

    def passive_recon(self, domain): #return an array of subdomain
        print(f"Passive reconnaissance for {domain}", file=sys.stderr)
        with ThreadPoolExecutor() as executor:
            futures = []
            for binary_name, arg_func in self.binaries.items():
                args = arg_func(domain)
                futures.append(executor.submit(Utilities.run_binary, binary_name, args))

            results = {future.result()[0]: future.result()[1] for future in as_completed(futures)}

        all_subdomains = set(sub for sublist in results.values() for sub in sublist)
        return all_subdomains

    def active_recon(self, domain,wl="./tmp/wordlist.txt"): #return an array of subdomain
        try:
            print(f"Starting active reconnaissance for domain: {domain}", file=sys.stderr)
            global knockpy_output
            knockpy_output = KNOCKPY(domain, dns=None, useragent=None, timeout=None, threads=None, recon=False, bruteforce=True, wordlist=None)
            return  [entry["domain"] for entry in knockpy_output]
        except subprocess.CalledProcessError as e:
            print(f"Error during active reconnaissance: {e.stderr}", file=sys.stderr)
            return []
        except FileNotFoundError as e:
            print("Error: 'knockpy' tool not found. Ensure it is properly installed and accessible.", file=sys.stderr)
            print(e, file=sys.stderr)
            return []
    def ip_port_collect(self, input_raw, iscommon=True):
        raw = ''
        input = input_raw
        if '*' in input_raw:
            input = input.replace('*', 'acktool')
        try:
            w = whois.whois(input)
        except Exception as e:
            raise ValueError(f"WHOIS lookup failed for {input}: {str(e)}")
            
        if not w.domain_name:
            raise ValueError(f"Invalid domain: {input_raw}")
        if iscommon:
            print(f"Scan commond port - {input_raw}",file=sys.stderr)
            raw = subprocess.run(["nmap", "-sV", input], check=True, text=True, capture_output=True)
        else:
            print(f"Scan all port - {input_raw}",file=sys.stderr)
            raw = subprocess.run(["nmap", "-p-", input], check=True, text=True, capture_output=True)
        result = raw.stdout.strip()
        res = Utilities.parse_nmap_output(result)
        if res != {}:
            return res
        return {
            input_raw: {}
        }
        
    def check_domain_status(self,domain):
        try:
            if '*' in domain:
                domain = domain.replace('*', 'acktool')
            # WHOIS để kiểm tra domain còn tồn tại không
            w = whois.whois(domain)
            if not w.domain_name:
                return {"status": "Not registered", "ip": []}
            
            # DNS để lấy IP
            ip_list = []
            try:
                ip_list.append(socket.gethostbyname(domain))
            except socket.gaierror:
                pass  # Không có IP
            
            return ip_list if ip_list else []
        except Exception as e:
            return []
    def ip_only(self, inputs): #return an array of IP
        if '*' in inputs:
            return []
        result = []
        try:
            raw = subprocess.run(["host", inputs], check=True, text=True, capture_output=True)
            tmp = raw.stdout.strip()
            for line in tmp.splitlines():
                parts = line.split()
                if len(parts) >= 4 and parts[2] in {"address", "IPv6"}:  # Ensure valid lines
                    ip = parts[-1]
                    result.append(ip)
        except subprocess.CalledProcessError:
            return []
        except Exception:
            return []
        return result
    
    def tech_collect_general(self,input):
        options = {
            "-td": "Technology detection",
            "-server": "Web server",
            "-tls-grab": "TLS fingerprint",
            "-asn": "ASN (Autonomous System Number)",
            "-ip": "IP address",
            "-cdn": "CDN",
            "-jarm": "TLS JARM fingerprint",
            "-cname": "CNAME domain",
            "-extract-fqdn": "Fully qualified domain name",
            "-sc": "HTTP status code",
            "-ct": "Content type",
            "-title": "Page title",
            "-method": "HTTP method",
            "-rt": "Response time",
            "-websocket": "WebSocket support",
        }
        try:
            w = whois.whois(input)
        except Exception as e:
            raise ValueError(f"WHOIS lookup failed for {input}: {str(e)}")
        if not w.domain_name:
            raise ValueError(f"Invalid domain: {input}")
        result = {}
        for option, meaning in options.items():
            output = subprocess.run(["/usr/bin/httpx",option,"-u", input], check=True, text=True, capture_output=True)
            raw = Utilities.remove_ansi_codes(output.stdout.strip())
            result[meaning] = Utilities.extract_result(raw,input)
        return result

    def url_collection(self, input_domain):
        try:
            w = whois.whois(input_domain)
        except Exception as e:
            raise ValueError(f"WHOIS lookup failed for {input_domain}: {str(e)}")
        if not w.domain_name:
            raise ValueError(f"Invalid domain: {input_domain}")
        with ThreadPoolExecutor() as executor:
            futures = []
            for binary_name, arg_func in self.urltools.items():
                args = arg_func(input_domain)
                futures.append(executor.submit(Utilities.run_binary, binary_name, args,input_domain))

            results = {future.result()[0]: future.result()[1] for future in as_completed(futures)}

        all_url = set(sub for sublist in results.values() for sub in sublist)
        fuzzed_urls = {Utilities.fuzzify_url(url) for url in all_url}
        print(f"{RED}URL collection found {len(fuzzed_urls)} URL.{RESET}",file=sys.stderr)
        return fuzzed_urls