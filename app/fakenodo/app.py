
from flask import Flask, request, jsonify
import uuid
from datetime import datetime

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
        return jsonify(
                {
                    "message": "Request badly formed",
                    "status": 400
                }
            )

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
        "title": metadata["title"],
        "submitted": False,
        "created": datetime.now().isoformat(),
        "files": [{}],
        "modify": datetime.now().isoformat(),
        "owner": 23,
        "record_url": "url",
        "state": "inprogress"
    }
    deposits[deposit_id] = new_deposit

    return jsonify({
        "message": "Deposit created successfully",
        "id": deposit_id,
        "doi": doi,
        "links": {
            "self": f"http://localhost:5000/api/deposit/depositions/{deposit_id}",
            "publish": f"http://localhost:5000/api/deposit/depositions/{deposit_id}/actions/publish",
            "edit": f"http://localhost:5000/api/deposit/depositions/{deposit_id}/actions/edit"
        }
    }), 201


@app.route('/api/deposit/depositions/<int:deposition_id>/files', methods=['POST'])
def upload_files(deposition_id):

    file = request.json
    print(file)
    return jsonify(file), 201
