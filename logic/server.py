from flask import Flask
from flask_cors import CORS
from controller import *
from flask import request
from routes.api_route import api_analysis_bp
from flask import jsonify
from collections.abc import Mapping

app = Flask(__name__)
CORS(app)  # ← This enables CORS for all routes

app.register_blueprint(api_analysis_bp)

#Member API Route
@app.route("/members",methods=["GET", "POST"])
def members():
    return {"member":["Member1","member2"]}

@app.route("/subdomains")
def subdomains():
    input_val = request.args.get("input")
    is_active = request.args.get("isactive")
    wordlist = request.args.get("wordlist")
    return jsonify(collect_subdomains(input_val,not is_active,wordlist))
@app.route("/checkdomains")
def checkdomains():
    input = request.args.get("input")
    ip_only = request.args.get("ipOnly")
    all_port = request.args.get("all_port")
    result = check_active_domains(input,ip_only, all_port)
    if isinstance(result, (Mapping, str)):
        return result
    return jsonify(result)

@app.route("/collectUrls")
def collect_res():
    input_val = request.args.get("input")
    wordlist = request.args.get("wordlist")
    res = collect_resources(input_val,wordlist)
    return jsonify(res[input_val])

@app.route("/scanTech")
def scan_tech():
    input_val = request.args.get("input")
    scanOS = request.args.get("scanOS")
    # firewall = request.args.get("firewall")
    result = scan_technologies(input_val)
    if isinstance(result, (Mapping, str)):
        print("K cần chuyển")
        print(result)
        return result
    print("chuyển")
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)