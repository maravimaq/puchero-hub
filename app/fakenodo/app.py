
from flask import Flask, request, jsonify
import uuid
from datetime import datetime
import hashlib
import os

app = Flask(__name__)

deposits = {}


@app.route('/api/deposit/depositions/<deposit_id>', methods=['GET'])
def get_deposit(deposit_id):
    deposit = deposits.get(deposit_id)
    if not deposit:
        return jsonify({"error": "Deposit not found"}), 404
    return jsonify(deposit), 200


@app.route('/api/deposit/depositions', methods=['POST'])
def create_deposit():
    data = request.get_json()

    if not data or 'title' not in data or 'description' not in data:
        return jsonify({
            "message": "Request badly formed",
            "status": 400
        }), 400

    deposit_id = str(uuid.uuid4())
    doi = f"10.5072/fakenodo.{uuid.uuid4().hex[:8]}"

    metadata = {
        "upload_type": "dataset",
        "title": data['title'],
        "description": data['description'],
        "publication_date": datetime.now().isoformat(),
        "creators": [{"name": "del Junco, Juan"}],
        "access_right": "open",
        "license": "cc-by-4.0"
    }

    new_deposit = {
        "id": deposit_id,
        "doi": doi,
        "metadata": metadata,
        "created": datetime.now().isoformat(),
        "submitted": False,
        "files": [],
        "owner": 23,
        "state": "inprogress"
    }
    deposits[deposit_id] = new_deposit

    return jsonify(new_deposit), 201


@app.route('/api/deposit/depositions/<deposit_id>/files', methods=['POST'])
def upload_files(deposit_id):
    deposit = deposits.get(deposit_id)
    if not deposit:
        return jsonify({"error": "Deposit not found"}), 404

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    file_id = str(uuid.uuid4())
    filename = file.filename

    temp_path = os.path.join('/tmp', filename)
    file.save(temp_path)

    # MD5 checksum
    md5_hash = hashlib.md5()
    with open(temp_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    checksum = f"md5:{md5_hash.hexdigest()}"

    filesize = os.path.getsize(temp_path)
    os.remove(temp_path)

    file_metadata = {
        "id": file_id,
        "filename": filename,
        "filesize": filesize,
        "checksum": checksum
    }

    deposit["files"].append(file_metadata)

    return jsonify(file_metadata), 201


@app.route('/api/deposit/depositions/<deposit_id>/files', methods=['GET'])
def list_files(deposit_id):
    deposit = deposits.get(deposit_id)
    if not deposit:
        return jsonify({"error": "Deposit not found"}), 404

    files = deposit.get("files", [])
    return jsonify(files), 200


@app.route('/api/deposit/depositions/<deposit_id>/files/<file_id>', methods=['GET'])
def get_file(deposit_id, file_id):
    deposit = deposits.get(deposit_id)
    if not deposit:
        return jsonify({"error": "Deposit not found"}), 404

    file_metadata = next((f for f in deposit["files"] if f["id"] == file_id), None)
    if not file_metadata:
        return jsonify({"error": "File not found"}), 404

    return jsonify(file_metadata), 200


@app.route('/api/deposit/depositions/<deposit_id>/files/<file_id>', methods=['DELETE'])
def delete_file(deposit_id, file_id):
    deposit = deposits.get(deposit_id)
    if not deposit:
        return jsonify({"error": "Deposit not found"}), 404

    if deposit.get("submitted"):
        return jsonify({"error": "Deleting a published deposition is forbidden"}), 403

    file_index = next((index for index, f in enumerate(deposit["files"]) if f["id"] == file_id), None)
    if file_index is None:
        return jsonify({"error": "File not found"}), 404

    deposit["files"].pop(file_index)

    return '', 204
