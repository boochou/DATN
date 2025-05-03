from flask import Blueprint, request, jsonify
from controllers.api_controller import *
from utils import *
import tempfile

api_analysis_bp = Blueprint("api-analysis", __name__)

@api_analysis_bp.route("/api/api-analysis/create-api-relationship", methods=["POST"])
def handle_create_api_relationship():
    if 'apisFile' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    uploaded_file = request.files['apisFile']
    
    if uploaded_file.filename == '':
        return jsonify({"error": "No selected file"}), 400


    # read content of uploaded file and process it
    uploaded_file_content = uploaded_file.read().decode('utf-8')
    parse_content = parse_requests_file_for_api_analysis(uploaded_file_content)
    r = llm_API_analysis(parse_content)
    if r['status'] == 200:
        try:
            flows = parse_llm_response_to_json_relationship(r['data'])
        except:
            flows = "Cannot convert response to flow."

        result = {
            "status": r["status"],
            "API_flows": flows,
            "raw_response": r["data"],
            "api_data": parse_content
        }
        return jsonify(result)
    
    return jsonify(r)

@api_analysis_bp.route("/api/recommend-tools", methods=["POST"])
def handle_recommend_tools():
    if request.content_type == "application/json":
        question = request.get_json()['question']
    else:
        question = request.form.get('question')
    time.sleep(0.1)
    r = {"status": 200, "data": "test data kakaka", "error": "there is error with the llm server"}

    r = llm_recommend_tool(question)
    
    return jsonify(r)


@api_analysis_bp.route("/api/basic-vulnerable-scanner", methods = ["POST"])
def handle_vuln_scanner():
    # def sqlmap scanner
    # def nuclei scanner
    
    pass

@api_analysis_bp.route("/api/sqli-scan", methods=["POST"])
def handle_sqlmap_scan():
    url = request.form.get("url")
    uploaded_file = request.files.get("file")

    # Check if both or neither are provided
    if (url and uploaded_file) or (not url and not uploaded_file):
        return jsonify({
            "status": 400,
            "error": "Provide either a URL or a request file, but not both."
        }), 400

    options = request.form.get('options')
    if (options):
        options = options.split(' ')

    try:
        if url:
            result = scan_sqlmap(url=url, options=options)
        else:
            file_content = uploaded_file.read().decode("utf-8")

            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as tmpfile:
                tmpfile.write(file_content)
                tmpfile_path = tmpfile.name

            result = scan_sqlmap(request=tmpfile_path, options=options)

            os.remove(tmpfile_path)  # Clean up temp file

        return jsonify({
            "status": 200,
            "result": result
        }), 200


        # Handle errors from sqlmap parsing
        if result.get("errors"):
            return jsonify({
                "status": 500,
                "error": result["errors"]
            }), 500

        return jsonify({
            "status": 200,
            "result": result
        }), 200

    except Exception as e:
        return jsonify({
            "status": 500,
            "error": str(e)
        }), 500