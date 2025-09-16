from flask import Flask, request, jsonify, send_file
from report_utils import generate_reports, delete_stale

app = Flask(__name__)

@app.route("/report", methods=["POST"])
def report():
    config = request.json
    result = generate_reports(config)
    return jsonify(result)

@app.route("/download/<file_name>", methods=["GET"])
def download(file_name):
    return send_file(file_name, as_attachment=True)

@app.route("/delete", methods=["POST"])
def delete():
    config = request.json
    deleted = delete_stale(config)
    return jsonify({"deleted": deleted, "count": len(deleted)})

if __name__ == "__main__":
    app.run(port=5001, debug=True)
