from flask import request, Request
import re
import json

def parse_requests_file_for_api_analysis(file_content) -> str:
    #extract http request - http response from file that contain api
    api_list = []
    entries = re.split(r'\n(?=POST|PUT|GET|PATCH|DELETE)', file_content.strip())
    
    for i, entry in enumerate(entries):
        req_match = re.search(r'^(POST|PUT|GET|PATCH|DELETE) .*? HTTP/(\d\.\d|2)(?:.|\n)*?(?=\nHTTP/1\.1 \d{3})', entry, re.MULTILINE | re.DOTALL)
        res_match = re.search(r'HTTP/(\d\.\d|2) \d{3}.*', entry, re.MULTILINE | re.DOTALL)
        
        req = req_match.group(0).strip() if req_match else ""
        res = res_match.group(0).strip() if res_match else ""
        
        if req:
            api_list.append({"id": len(api_list), "req": req, "res": res})
    
    #convert api_list to suitable format for llm input
    result_input = ""
    for item in api_list:
        result_input += f"[API_{item['id']}]\n{item['req']}\n\n{item['res']}\n\n[end API_{item['id']}]\n\n\n"
    return result_input

def extract_parameter(line: str):
    url_prefix = "#url#"
    header_prefix = "#hd#"
    param_prefix = "#p#"

    parts = line.split('and API ')
    res = []
    for part in parts:
        if part.find("has parameter") != -1:
            res += [param_prefix + re.search(r"'(.*?)'", part).group(1)]
        elif part.find("has url") != -1:
            res += [url_prefix + re.findall(r"\d+", part)[0]]
        else:
            res += [header_prefix + re.search(r"'(.*?)'", part).group(1)]
    return res

def parse_llm_response_to_json_relationship(llm_res):
    data_split = llm_res.split('\n')[3:]
    res = {"flows":[]}
    dict_reason = {}
    for data_line in data_split:
        parts = data_line.split(". Reason:")
        #extract api that revelant
        apis = '_'.join(re.findall(r'\d+', parts[0]))

        #extract param, header, url key and their value
        keys_value = parts[1].split("with the same value")

        rs = extract_parameter(keys_value[0]) + [keys_value[1].strip(" '")]
        if dict_reason.get(apis):
            dict_reason[apis] += [rs]
        else:
            dict_reason[apis] = [rs]

    for key, value in dict_reason.items():
        res['flows'] += [{
            "apis":key.split('_'),
            "reasons": [{
                key: value
            }]

        }]
    return res