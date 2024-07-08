from flask import Flask, request, jsonify, send_file
import io
import os
from abcvlib.setup_config import main as setup_config_main

app = Flask(__name__)

DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), '../../data')

@app.route("/", methods=["POST"])
def handle_post_request():
    print(f"Received request with headers: {request.headers}")
    data_type = request.headers.get("Data-Type")

    if data_type == "string":
        data = request.data.decode("utf-8")
        print(f"Received string: {data}")
        response = "String received"
    elif data_type == "file":
        file_name = request.headers.get("File-Name")
        file_size = int(request.headers.get("File-Size"))
        file_type = request.headers.get("File-Type")
        file_data = request.data
        print(f"Received file: {file_name} of size {file_size} and type {file_type}")
        response = "File received"
    elif data_type == "flatbuffer":
        flatbuffer_name = request.headers.get("Flatbuffer-Name")
        flatbuffer_size = int(request.headers.get("Flatbuffer-Size"))
        flatbuffer_data = request.data
        print(f"Received flatbuffer: {flatbuffer_name} of size {flatbuffer_size}")
        response = "Flatbuffer received"
    else:
        response = "Unknown data type"

    return jsonify({"status": response}), 200


@app.route("/file", methods=["GET"])
def handle_get_request():
    filename = request.args.get("filename")  # Get the filename from query parameters
    if not filename:
        return jsonify({"status": "error", "message": "Filename is required"}), 400

    file_path = os.path.join(DATA_DIRECTORY, filename)  # Define the directory where files are stored

    if not os.path.isfile(file_path):
        return jsonify({"status": "error", "message": "File not found"}), 404

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    print("Running setup_config...")
    setup_config_main()

    app.run(host="0.0.0.0", port=5000, debug=True)
