from flask import Flask
from flask_cors import CORS
from acktool import *
from flask import request
app = Flask(__name__)
CORS(app)  # ← This enables CORS for all routes

#Member API Route
@app.route("/members")
def members():
    return {"member":["Member1","member2"]}

@app.route("/subdomains")
def subdomains():
    input_val = request.args.get("input")
    is_active = request.args.get("isactive")
    wordlist = request.args.get("wordlist")
    return collect_subdomains(input_val,not is_active,wordlist)
@app.route("/checkdomains")
def checkdomains():
    input = request.args.get("input")
    ip_only = request.args.get("ipOnly")
    all_port = request.args.get("all_port")
    return check_active_domains(input,ip_only, all_port)

if __name__ == "__main__":
    app.run(debug=True)