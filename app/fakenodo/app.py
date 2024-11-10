from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/deposit/depositions", methods=['GET'])
def get_depositions():
    data = [{
        "conceptrecid": "542200",
        "created": "2020-05-19T11:58:41.606998+00:00",
        "files": [],
        "id": 542201,
        "links": {
            "bucket": "https://zenodo.org/api/files/568377dd-daf8-4235-85e1-a56011ad454b",
            "discard": "https://zenodo.org/api/deposit/depositions/542201/actions/discard",
            "edit": "https://zenodo.org/api/deposit/depositions/542201/actions/edit",
            "files": "https://zenodo.org/api/deposit/depositions/542201/files",
            "html": "https://zenodo.org/deposit/542201",
            "latest_draft": "https://zenodo.org/api/deposit/depositions/542201",
            "latest_draft_html": "https://zenodo.org/deposit/542201",
            "publish": "https://zenodo.org/api/deposit/depositions/542201/actions/publish",
            "self": "https://zenodo.org/api/deposit/depositions/542201"
        },
        "metadata": {
            "prereserve_doi": {
                "doi": "10.5072/zenodo.542201",
                "recid": 542201
            }
        },
        "modified": "2020-05-19T11:58:41.607012+00:00",
        "owner": 12345,
        "record_id": 542201,
        "state": "unsubmitted",
        "submitted": False,
        "title": ""
    }]
    return jsonify(data), 200


@app.route('/api/deposit/', methods=['POST'])
def create_deposit():
    return jsonify({"message": "Deposit created successfully"}), 201
