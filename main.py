import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import csv
from knock import KNOCKPY
import json
import os
import re

output_dir = "results"
knockpy_output=''
class Utilities:
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
            print(f"{binary_name} found {len(output)} subdomains.")           
            return binary_name, output
        except subprocess.CalledProcessError as e:
            print(f"Error running {binary_name}: {e.stderr}")
            return binary_name, []
        except FileNotFoundError:
            print(f"Error: The binary '{binary_name}' was not found. Make sure it is installed and in your PATH.")
            return binary_name, []
    @staticmethod
    def fuzzify_url(url):
        pattern = r'(?<==)([^&#/?]+)'  # Tìm giá trị ngay sau dấu '=' và trước ký tự đặc biệt
        fuzzed_url = re.sub(pattern, 'FUZZ', url)
        return fuzzed_url
    @staticmethod
    def extract_result(output, domain):
        match = re.search(rf"{re.escape(domain)}\s*\[(.*?)\]", output)
        return match.group(1) if match else None
    
    @staticmethod
    def remove_ansi_codes(text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

class Reconn:
    def __init__(self):
        self.binaries = {
            "subfinder": lambda domain: ["-d", domain],
            "assetfinder": lambda domain: [domain]
        }

    def passive_recon(self, domain):
        with ThreadPoolExecutor() as executor:
            futures = []
            for binary_name, arg_func in self.binaries.items():
                args = arg_func(domain)
                futures.append(executor.submit(Utilities.run_binary, binary_name, args))

            results = {future.result()[0]: future.result()[1] for future in as_completed(futures)}

        all_subdomains = set(sub for sublist in results.values() for sub in sublist)
        print(f"Passive recon found {len(all_subdomains)} unique subdomains.")
        return all_subdomains

    def active_recon(self, domain):
        try:
            print(f"Starting active reconnaissance for domain: {domain}")
            global knockpy_output
            knockpy_output = KNOCKPY(domain, dns=None, useragent=None, timeout=None, threads=None, recon=False, bruteforce=True, wordlist="./tmp/dict.txt")
            return  [entry["domain"] for entry in knockpy_output]
        except subprocess.CalledProcessError as e:
            print(f"Error during active reconnaissance: {e.stderr}")
            return []
        except FileNotFoundError:
            print("Error: 'knockpy' tool not found. Ensure it is properly installed and accessible.")
            return []

    def ip_port_collect(self, input_file):
        try:
            print(f"Running nmap on file: {input_file}")
            result = subprocess.run(["nmap", "-iL", input_file, "-sV"], check=True, text=True, capture_output=True)
            nmap_output = result.stdout.strip()
            print("Nmap scan completed. Processing results...")

            subfolder_path = os.path.join(output_dir, "ip_port")
            os.makedirs(subfolder_path, exist_ok=True)
            output_file = os.path.join(subfolder_path, f"nmap_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            
            with open(output_file, "w", newline="") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(["Domain", "IP", "Port", "State", "Service", "IPv6"])  # Header CSV

                current_domain = None
                current_ip = None
                current_ipv6 = None

                for line in nmap_output.splitlines():
                    if "Nmap scan report for" in line:
                        parts = line.split(" ")
                        current_domain = parts[-1].strip("()")
                        current_ip = parts[-2] if len(parts) > 2 else "Unknown"
                        current_ipv6 = None  # Reset IPv6

                    elif "IPv6 address" in line:
                        current_ipv6 = line.split()[-1]

                    elif "/tcp" in line and current_domain:
                        port_info = line.split()
                        port = port_info[0].split('/')[0]  # port
                        state = port_info[1]  # State (open, closed,...)
                        service = port_info[2] if len(port_info) > 2 else "Unknown"

                        csv_writer.writerow([current_domain, current_ip, port, state, service, current_ipv6])

            print(f"IP/Port collection completed. Results saved to '{output_file}'.")

        except subprocess.CalledProcessError as e:
            print(f"Error running nmap: {e.stderr}")
        except FileNotFoundError:
            print("Error: 'nmap' binary not found. Ensure it is installed and accessible.")
class Collections:
    def  __init__(self):
        self.urltools = {
            "paramspider": lambda domain: ["-d", domain],
            "katana": lambda domain: ["-u", domain]
        }
    def url_collection(self, input_domain):
        with ThreadPoolExecutor() as executor:
            futures = []
            for binary_name, arg_func in self.urltools.items():
                args = arg_func(input_domain)
                futures.append(executor.submit(Utilities.run_binary, binary_name, args,input_domain))

            results = {future.result()[0]: future.result()[1] for future in as_completed(futures)}

        all_url = set(sub for sublist in results.values() for sub in sublist)
        fuzzed_urls = {Utilities.fuzzify_url(url) for url in all_url}
        print(f"URL collection found {len(fuzzed_urls)} URL.")
        return fuzzed_urls
    def run_httpx_command(self,command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return Utilities.remove_ansi_codes(result.stdout.strip())
        except Exception as e:
            return str(e)
    def technology_collection(self,input_domain):
        base_url = f"https://{input_domain}"
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
        subfolder_path = os.path.join(output_dir, "technology_collection")
        os.makedirs(subfolder_path, exist_ok=True)
        output_file = os.path.join(subfolder_path, f"{input_domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(output_file, "w") as file:
            file.write(input_domain + "\n--------------------------------\n")
            for option, meaning in options.items():
                command = f"/usr/bin/httpx -u {input_domain} {option}"
                output = self.run_httpx_command(command)
                # Extract only the relevant result
                result = Utilities.extract_result(output, base_url)
                if result:
                    final_output = f"{meaning}: {result}"
                    print(final_output)
                    file.write(final_output + "\n")

if __name__ == "__main__":
    os.makedirs(output_dir, exist_ok=True)
    print("Choose an operation:")
    print("1. Recon")
    print("2. IP/Port Collection")
    print("3. Technology Collection")
    print("4. URL Collection")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        domain = input("Enter a single domain for reconnaissance: ").strip()
        if not domain:
            print("No domain provided. Exiting.")
        else:
            reconn_tool = Reconn()

            # Run both passive and active reconnaissance concurrently
            with ThreadPoolExecutor() as executor:
                passive_future = executor.submit(reconn_tool.passive_recon, domain)
                recon_type = input("Do you want to perform active reconnaissance? (y/n): ").strip().lower()
                active_future = executor.submit(reconn_tool.active_recon, domain) if recon_type == "y" else None

                # Wait for tasks to complete
                passive_results = passive_future.result()
                active_results = active_future.result() if active_future else []

            # Combine results
            all_results = sorted(set(passive_results).union(active_results))
            
            subfolder_path = os.path.join(output_dir, "reconn")
            os.makedirs(subfolder_path, exist_ok=True)
            # Generate output file
            output_file = os.path.join(subfolder_path, f"{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(output_file, "w") as file:
                file.write("\n".join(all_results))

            print(f"Reconnaissance completed. Found {len(all_results)} unique subdomains ({len(passive_results)} passive & {len(active_results)} active). Results saved to '{output_file}'.")

            collect_ip_port = input("Do you want to collect IP/Port information using nmap? (y/n): ").strip().lower()
            if collect_ip_port == "y":
                if os.path.exists(output_file):
                    reconn_tool.ip_port_collect(output_file)
                else:
                    print(f"Error: File '{output_file}' does not exist.")

    elif choice == "2":
        input_file = input("Enter the path to the input file for IP/Port collection: ").strip()
        if not os.path.exists(input_file):
            print(f"Error: File '{input_file}' does not exist.")
        else:
            reconn_tool = Reconn()
            reconn_tool.ip_port_collect(input_file)
    elif choice =="3":
        input_domain = input("Enter your domain for technologyn: ").strip()
        technology_collect = Collections()
        if not input_domain:
            print("No domain provided. Exiting.")
        else:
            technology_collect.technology_collection(input_domain)
    elif choice == "4":
        input_domain = input("Enter your domain for URL collection: ").strip()
        url_collect = Collections()
        if not input_domain:
            print("No domain provided. Exiting.")
        else:
            collected_urls = url_collect.url_collection(input_domain)
            subfolder_path = os.path.join(output_dir, "url_collection")
            os.makedirs(subfolder_path, exist_ok=True)

            output_file = os.path.join(subfolder_path, f"{input_domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(output_file, "w") as file:
                file.write("\n".join(collected_urls))
            print(f"URL collection completed. Found {len(collected_urls)} URLs. Results saved to '{output_file}'.")
        
    else:
        print("Invalid choice. Exiting.")