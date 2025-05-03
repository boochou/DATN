import requests
import json
import time
from dotenv import load_dotenv
import os
import subprocess
import re

load_dotenv()

# Set up the base URL for the local Ollama API
BASE_URL = os.getenv('LLMURL')
MODEL = os.getenv('MODEL')
url = f"{BASE_URL}/api/generate"

def llm_API_analysis(input_apis_list):
    alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

    ### Instruction:
    {}

    ### Input:
    {}

    ### Response:
    {}"""

    prompt = alpaca_prompt.format(
        "Create API relationship of the following APIs", # instruction
        input_apis_list,
        "", # output - leave this blank for generation!
    )

    payload = {
        "model": MODEL,
        "prompt": prompt
    }

    result = """Relationship of the APIs:


API 0 and 1. Reason: API 0 has parameter '$accountType' and API 1 has url segment num 2 with the same value 'Savings'
API 0 and 1. Reason: API 0 has parameter '$accountId' and API 1 has parameter '$accountId' with the same value 'ACCT12345'
API 0 and 2. Reason: API 0 has parameter '$accountId' and API 2 has url segment num 2 with the same value 'ACCT12345'
API 0 and 3. Reason: API 0 has parameter '$accountId' and API 3 has parameter '$accountId' with the same value 'ACCT12345'
API 0 and 5. Reason: API 0 has parameter '$accountId' and API 5 has parameter '$fromAccountId' with the same value 'ACCT12345'
API 1 and 2. Reason: API 1 has url segment num 2 and API 2 has parameter '$accountId' with the same value 'ACCT12345'
API 1 and 3. Reason: API 1 has url segment num 2 and API 3 has parameter '$accountId' with the same value 'ACCT12345'
API 1 and 4. Reason: API 1 has parameter '$amount' and API 4 has parameter '$[0].$amount' with the same value '500'
API 1 and 5. Reason: API 1 has url segment num 2 and API 5 has parameter '$fromAccountId' with the same value 'ACCT12345'
API 1 and 16. Reason: API 1 has parameter '$accountId' and API 16 has parameter '$accountId' with the same value 'ACCT12345'
API 3 and 4. Reason: API 3 has url segment num 2 and API 4 has parameter '$[1].$amount' with the same value '-200'
API 3 and 5. Reason: API 3 has url segment num 2 and API 5 has parameter '$fromAccountId' with the same value 'ACCT12345'
API 3 and 16. Reason: API 3 has parameter '$accountId' and API 16 has parameter '$accountId' with the same value 'ACCT12345'
API 4 and 5. Reason: API 4 has parameter '$[0].$transactionId' and API 5 has parameter '$transactionId' with the same value 'TXN67890'
API 4 and 6. Reason: API 4 has url segment num 2 and API 6 has parameter '$accountId' with the same value 'ACCT12345'
API 4 and 8. Reason: API 4 has url segment num 2 and API 8 has parameter '$[0]' with the same value 'ACCT12345'
API 4 and 16. Reason: API 4 has url segment num 2 and API 16 has parameter '$accountId' with the same value 'ACCT12345'
API 5 and 6. Reason: API 5 has parameter '$toAccountId' and API 6 has parameter '$accountId' with the same value 'ACCT65432'
API 5 and 8. Reason: API 5 has url segment num 2 and API 8 has parameter '$[0]' with the same value 'ACCT12345'
API 5 and 16. Reason: API 5 has parameter '$fromAccountId' and API 16 has parameter '$accountId' with the same value 'ACCT12345'
API 6 and 7. Reason: API 6 has parameter '$customerId' and API 7 has url segment num 2 with the same value 'CUST123'
API 6 and 8. Reason: API 6 has parameter '$accountId' and API 8 has parameter '$[0]' with the same value 'ACCT12345'
API 6 and 11. Reason: API 6 has parameter '$accountId' and API 11 has parameter '$accountId' with the same value 'ACCT12345'
API 6 and 16. Reason: API 6 has parameter '$accountId' and API 16 has url segment num 2 with the same value 'ACCT12345'
API 7 and 8. Reason: API 7 has url segment num 2 and API 8 has parameter '$[0]' with the same value 'ACCT12345'
API 7 and 11. Reason: API 7 has url segment num 2 and API 11 has parameter '$accountId' with the same value 'ACCT12345'
API 7 and 16. Reason: API 7 has url segment num 2 and API 16 has parameter '$accountId' with the same value 'ACCT12345'
API 8 and 9. Reason: API 8 has parameter '$[0]' and API 9 has parameter '$loanAmount' with the same value '1000'
API 8 and 10. Reason: API 8 has parameter '$[0]' and API 10 has parameter '$loanId' with the same value 'LOAN12345'
API 8 and 16. Reason: API 8 has parameter '$[0]' and API 16 has url segment num 2 with the same value 'ACCT12345'
API 9 and 10. Reason: API 9 has parameter '$loanId' and API 10 has url segment num 3 with the same value 'LOAN12345'
API 11 and 12. Reason: API 11 has parameter '$accountId' and API 12 has url segment num 2 with the same value 'ACCT12345'
API 11 and 16. Reason: API 11 has parameter '$accountId' and API 16 has parameter '$accountId' with the same value 'ACCT12345'"""
    # return {"status": 200, "data": result}
    response = requests.post(url, json=payload, stream=True)
    if response.status_code == 200:
        result = ""
        for line in response.iter_lines(decode_unicode=True):
            if line:
                data = json.loads(line)
                result += data.get("response", "")
        return {"status": 200, "data": result}
    
    return {"status": 500, "error": "LLM Server error, please try again"}

def llm_recommend_tool(question):
    alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

    ### Instruction:
    {}

    ### Input:
    {}

    ### Response:
    {}"""

    prompt = alpaca_prompt.format(
        "Answer the following question as a professtional pentester", # instruction
        question,
        "", # output - leave this blank for generation!
    )

    payload = {
        "model": MODEL,
        "prompt": prompt
    }

    response = requests.post(url, json=payload, stream=True)
    if response.status_code == 200:
        result = ""
        for line in response.iter_lines(decode_unicode=True):
            if line:
                data = json.loads(line)
                result += data.get("response", "")
        return {"status": 200, "data": result}
    
    return {"status": 500, "error": "LLM Server error, please try again"}
    
def scan_sqlmap(**kwargs):
    """
    Scan using sqlmap. Accepts either 'url' or 'request' as keyword arguments.
    
    Args:
        url (str): Target URL to scan.
        request (str): Path to a request file to scan.
        options (list): Optional list of extra sqlmap options (e.g., ["--batch", "--dbs"]).

    Returns:
        str: Parsed result from sqlmap output.
    """
    cmd = ["sqlmap", "--batch"]

    if "url" in kwargs:
        cmd += ["-u", kwargs["url"]]
    elif "request" in kwargs:
        cmd += ["-r", kwargs["request"]]
    else:
        raise ValueError("You must provide either 'url' or 'request' as argument.")

    if "options" in kwargs and isinstance(kwargs["options"], list):
        cmd += kwargs["options"]

    try:
        print(cmd)
        sql_result_process = subprocess.run(cmd, check=True, text=True, capture_output=True)
        raw_result = sql_result_process.stdout.strip()
        print(raw_result)
        result = parse_sqlmap_result(raw_result)
        return result
    except subprocess.CalledProcessError as e:
        return f"Error running sqlmap: {e.stderr.strip()}"


def parse_sqlmap_result(output):
    return output
    result = {
        "vulnerable": False,
        "dbms": None,
        "techniques": [],
        "databases": []
    }

    # Check if injectable
    if re.search(r"parameter.+appears to be injectable", output, re.IGNORECASE):
        result["vulnerable"] = True

    # Find DBMS
    dbms_match = re.search(r"back-end DBMS is ['\"]?(\w+)['\"]?", output)
    if dbms_match:
        result["dbms"] = dbms_match.group(1)

    # Find SQLi techniques used
    techniques = re.findall(r"testing '([^']+)'", output)
    result["techniques"] = list(set(techniques))  # remove duplicates

    # Extract available databases
    db_matches = re.findall(r"\[\*\] (\w+)", output)
    if db_matches:
        result["databases"] = db_matches

    error_lines = []
    for line in output.splitlines():
        if any(level in line for level in ["[CRITICAL]", "[ERROR]", "[WARNING]"]):
            clean_line = re.sub(r"\[\w+\]\s*", "", line).strip()
            error_lines.append(clean_line)
    result["errors"] = error_lines

    return result