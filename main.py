import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import csv
from knock import KNOCKPY
import json
import os

output_dir = "output"
knockpy_output=''
class Utilities:
    @staticmethod
    def run_binary(binary_name, arguments):
        try:
            result = subprocess.run([binary_name] + arguments, check=True, text=True, capture_output=True)
            output = result.stdout.strip().splitlines()
            print(f"{binary_name} found {len(output)} subdomains.")
            return binary_name, output
        except subprocess.CalledProcessError as e:
            print(f"Error running {binary_name}: {e.stderr}")
            return binary_name, []
        except FileNotFoundError:
            print(f"Error: The binary '{binary_name}' was not found. Make sure it is installed and in your PATH.")
            return binary_name, []

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

if __name__ == "__main__":
    os.makedirs(output_dir, exist_ok=True)
    print("Choose an operation:")
    print("1. Recon")
    print("2. IP/Port Collection")
    choice = input("Enter your choice (1/2): ").strip()

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

    else:
        print("Invalid choice. Exiting.")