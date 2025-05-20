import json
import os
import re
import sys
import subprocess
from collections import Counter
from knock import KNOCKPY
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import socket
import whois
import multiprocessing
# Python 2.x and 3.x compatiablity
if sys.version > '3':
    import urllib.parse as urlparse
    import urllib.parse as urllib
else:
    import urlparse
    import urllib

# In case you cannot install some of the required development packages
# there's also an option to disable the SSL warning:
try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except:
    pass
RED = "\033[91m"
RESET = "\033[0m"  # Reset về màu mặc định
# Check if we are running this on windows platform
is_windows = sys.platform.startswith('win')

# Console Colors
if is_windows:
    # Windows deserves coloring too :D
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white
    try:
        import win_unicode_console , colorama
        win_unicode_console.enable()
        colorama.init()
        #Now the unicode will work ^_^
    except:
        print("[!] Error: Coloring libraries not installed, no coloring will be used [Check the readme]")
        G = Y = B = R = W = G = Y = B = R = W = ''


else:
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white





class enumratorBase(object):
    def __init__(self, base_url, engine_name, domain, subdomains=None, silent=False, verbose=True):
        subdomains = subdomains or []
        self.domain = urlparse.urlparse(domain).netloc
        self.session = requests.Session()
        self.subdomains = []
        self.timeout = 25
        self.base_url = base_url
        self.engine_name = engine_name
        self.silent = silent
        self.verbose = verbose
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Accept-Encoding': 'gzip',
        }
        self.print_banner()

    def print_(self, text):
        if not self.silent:
            print(text)
        return

    def print_banner(self):
        """ subclass can override this if they want a fancy banner :)"""
        # self.print_(G + "[-] Searching now in %s.." % (self.engine_name) + W)
        return

    def send_req(self, query, page_no=1):
        url = self.base_url.format(query=query, page_no=page_no)
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception:
            resp = None
        return self.get_response(resp)

    def get_response(self, response):
        if response is None:
            return 0
        return response.text if hasattr(response, "text") else response.content

    def check_max_subdomains(self, count):
        if self.MAX_DOMAINS == 0:
            return False
        return count >= self.MAX_DOMAINS

    def check_max_pages(self, num):
        if self.MAX_PAGES == 0:
            return False
        return num >= self.MAX_PAGES

    # override
    def extract_domains(self, resp):
        """ chlid class should override this function """
        return

    # override
    def check_response_errors(self, resp):
        """ chlid class should override this function
        The function should return True if there are no errors and False otherwise
        """
        return True

    def should_sleep(self):
        """Some enumrators require sleeping to avoid bot detections like Google enumerator"""
        return

    def generate_query(self):
        """ chlid class should override this function """
        return

    def get_page(self, num):
        """ chlid class that user different pagnation counter should override this function """
        return num + 10

    def enumerate(self, altquery=False):
        flag = True
        page_no = 0
        prev_links = []
        retries = 0

        while flag:
            query = self.generate_query()
            count = query.count(self.domain)  # finding the number of subdomains found so far
            # if they we reached the maximum number of subdomains in search query
            # then we should go over the pages
            if self.check_max_subdomains(count):
                page_no = self.get_page(page_no)

            if self.check_max_pages(page_no):  # maximum pages for Google to avoid getting blocked
                return self.subdomains
            resp = self.send_req(query, page_no)

            # check if there is any error occured
            if not self.check_response_errors(resp):
                return self.subdomains
            links = self.extract_domains(resp)
            # if the previous page hyperlinks was the similar to the current one, then maybe we have reached the last page
            if links == prev_links:
                retries += 1
                page_no = self.get_page(page_no)
            else:
                self.subdomains.extend(links)

        # make another retry maybe it isn't the last page
                if retries >= 3:
                    return self.subdomains

            prev_links = links
            self.should_sleep()
        return self.subdomains


class enumratorBaseThreaded(multiprocessing.Process, enumratorBase):
    def __init__(self, base_url, engine_name, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        enumratorBase.__init__(self, base_url, engine_name, domain, subdomains, silent=silent, verbose=verbose)
        multiprocessing.Process.__init__(self)
        self.q = q
        return

    def run(self):
        domain_list = self.enumerate()
        for domain in domain_list:
            self.q.append(domain)


class YahooEnum(enumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = "https://search.yahoo.com/search?p={query}&b={page_no}"
        self.engine_name = "Yahoo"
        self.MAX_DOMAINS = 30
        self.MAX_PAGES = 100
        super(YahooEnum, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        self.q = q
        return

    def extract_domains(self, resp):
        with open("yahoo.html", "w", encoding="utf-8") as file:
            file.write(resp)
        domain_regex = re.escape(self.domain)
        # Regex pattern: tìm các chuỗi có dạng >something.example.com<
        link_regx = re.compile(rf">([^<]*?\.{domain_regex})<")

        links_set = set()  # Khởi tạo một tập hợp để lưu các liên kết

        try:
            matches = link_regx.findall(resp)  # Tìm kiếm các liên kết trong nội dung phản hồi
            for link in matches:
                if link not in links_set:  # Kiểm tra xem liên kết đã có trong tập hợp chưa
                    links_set.add(link)  # Thêm liên kết vào tập hợp
                    # print(link)
        except Exception as e:
            print(f"Lỗi xảy ra: {e}")

        links_list = list(links_set)  # Chuyển đổi tập hợp sang danh sách
        return links_list

    def should_sleep(self):
        return

    def get_page(self, num):
        return num + 10

    def generate_query(self):
        if self.subdomains:
            fmt = 'site:{domain} -domain:www.{domain} -domain:{found}'
            found = ' -domain:'.join(self.subdomains[:77])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "site:{domain} -domain:www.{domain}".format(domain=self.domain)
        return query


class BingEnum(enumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://www.bing.com/search?q={query}&go=Submit&first={page_no}'
        self.engine_name = "Bing"
        self.MAX_DOMAINS = 30
        self.MAX_PAGES = 100
        enumratorBaseThreaded.__init__(self, base_url, self.engine_name, domain, subdomains, q=q, silent=silent)
        self.q = q
        self.verbose = verbose
        return
    def extract_domains(self, resp):
        links_list = list()
        links_set = set()  # Khởi tạo một tập hợp để lưu các liên kết

        link_regx = re.compile('<cite.*?>(.*?)<\/cite>')
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
                print("hi", link)
                link = re.sub(r'https?://', '', link)
                link = link.split('›')[0]
                if link not in links_set: 
                    links_set.add(link)
        except Exception:
            pass
        links_list = list(links_set)
        return links_list


    def generate_query(self):
        if self.subdomains:
            fmt = 'domain:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.subdomains[:self.MAX_DOMAINS])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "{domain}".format(domain=self.domain)
        return query



def main(domain, threads=None, savefile=None, ports=None, silent=None, verbose=None, enable_bruteforce=None, engines=None):
    search_list = set()
    # print("CALL ME")
    if is_windows:
        subdomains_queue = list()
    else:
        subdomains_queue = multiprocessing.Manager().list()
    # Validate domain
    domain_check = re.compile("^(http|https)?[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$")
    if not domain_check.match(domain):
        if not silent:
            print(R + "Error: Please enter a valid domain" + W)
        return []

    if not domain.startswith('http://') or not domain.startswith('https://'):
        domain = 'http://' + domain

    supported_engines = {
                         'yahoo': YahooEnum,
                         'bing': BingEnum
                         }

    chosenEnums = []

    if engines is None:
        chosenEnums = [
             YahooEnum,
             BingEnum
        ]
    else:
        engines = engines.split(',')
        for engine in engines:
            if engine.lower() in supported_engines:
                chosenEnums.append(supported_engines[engine.lower()])

    # Start the engines enumeration
    enums = [enum(domain, [], q=subdomains_queue, silent=silent, verbose=verbose) for enum in chosenEnums]
    for enum in enums:
        enum.start()
    for enum in enums:
        enum.join()
    subdomains = set(subdomains_queue)
    for subdomain in subdomains:      
        search_list.add(subdomain)
    
    return "searchEngine", list(subdomains)

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
         # Danh sách các domain cần loại bỏ
        blocked_domains = {'motchillphim.biz', 'doubledandt.click', 'livexd.smartroom.vn'}
        
        # Lọc bỏ các domain không mong muốn
        results = [r for r in results if r not in blocked_domains]
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
            futures.append(executor.submit(main, domain))
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
            # w = whois.whois(domain)
            # if not w.domain_name:
            #     return {"status": "Not registered", "ip": []}
            
            # DNS để lấy IP
            # ip_list = []
            result = []
            raw = subprocess.run(["host",domain], check=True, text=True, capture_output=True)
            tmp = raw.stdout.strip() 
            for line in tmp.splitlines():

                parts = line.split()
                if len(parts) >= 4 and parts[2] in {"address", "IPv6"}:  # Ensure valid lines
                    ip = parts[-1]
                    result.append(ip)
            
            return result if result else []
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
    
    def tech_collect_general(self, input):
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


        result = {}

        def run_option(option, meaning):
            try:
                output = subprocess.run(
                    ["/usr/bin/httpx", option, "-u", input],
                    check=True,
                    text=True,
                    capture_output=True
                )
                raw = Utilities.remove_ansi_codes(output.stdout.strip())
                return meaning, Utilities.extract_result(raw, input)
            except Exception as e:
                return meaning, f"Error: {e}"

        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = {executor.submit(run_option, opt, desc): opt for opt, desc in options.items()}
            for future in as_completed(futures):
                meaning, value = future.result()
                result[meaning] = value

        return result

    def url_collection(self, input_domain):
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