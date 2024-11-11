import pytest
from app import app, deposits
import os

FAKENODO_API_URL = os.environ["ZENODO_API_URL"]


@pytest.fixture
def test_client():
    """Fixture for setting up a Flask test client."""
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_deposits():
    """Clear the deposits dictionary before each test to ensure isolation."""
    deposits.clear()


def test_create_deposit_missing_fields(test_client):
    """Test creating a deposit with missing fields. Required fields are title and description.
    """
    response = test_client.post('/api/deposit/depositions', json={"title": "Incomplete Deposit"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "Request badly formed"


def test_list_files(test_client):
    """Test listing all files in a deposit."""
    response = test_client.post('/api/deposit/depositions', json={
        "title": "Test Deposit",
        "description": "This is a test deposit"
    })
    deposit_id = response.get_json()["id"]

    with open("sample.txt", "w") as f:
        f.write("This is a sample file.")
    with open("sample.txt", "rb") as f:
        test_client.post(f'/api/deposit/depositions/{deposit_id}/files', data={"file": (f, "sample.txt")})

    response = test_client.get(f'/api/deposit/depositions/{deposit_id}/files')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0

    os.remove("sample.txt")


def test_update_file(test_client):
    """Test updating a file's name in a deposit."""
    response = test_client.post('/api/deposit/depositions', json={
        "title": "Test Deposit",
        "description": "This is a test deposit"
    })
    deposit_id = response.get_json()["id"]

    with open("sample.txt", "w") as f:
        f.write("This is a sample file.")
    with open("sample.txt", "rb") as f:
        response = test_client.post(f'/api/deposit/depositions/{deposit_id}/files', data={"file": (f, "sample.txt")})

    file_id = response.get_json()["id"]
    response = test_client.put(f'/api/deposit/depositions/{deposit_id}/files/{file_id}',
                               json={"filename": "renamed.txt"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["filename"] == "renamed.txt"

    os.remove("sample.txt")


def test_delete_file(test_client):
    """Test deleting a file from a deposit."""
    response = test_client.post('/api/deposit/depositions', json={
        "title": "Test Deposit",
        "description": "This is a test deposit"
    })
    deposit_id = response.get_json()["id"]

    with open("sample.txt", "w") as f:
        f.write("This is a sample file.")
    with open("sample.txt", "rb") as f:
        file_response = test_client.post(f'/api/deposit/depositions/{deposit_id}/files',
                                         data={"file": (f, "sample.txt")})
    file_id = file_response.get_json()["id"]

    delete_response = test_client.delete(f'/api/deposit/depositions/{deposit_id}/files/{file_id}')
    assert delete_response.status_code == 204

    response = test_client.get(f'/api/deposit/depositions/{deposit_id}/files/{file_id}')
    assert response.status_code == 404

    os.remove("sample.txt")


def test_crud_deposition(test_client):
    """
    First create a deposition, then upload a test file to that deposition
    and delete the deposition.
    """

    file_path = "test_file.txt"
    with open(file_path, "w") as f:
        f.write("This is a test file with some content.")

    deposition_data = {
        "title": "Test Deposition",
        "description": "This is a test deposition created via Fakenodo API",
    }

    response = test_client.post(FAKENODO_API_URL, json=deposition_data)

    assert response.status_code == 201, "Has failed."
    assert response.get_json()["id"]
    assert isinstance(response.get_json()["id"], int)
    assert response.get_json()["metadata"]
    assert response.get_json()["metadata"]["title"] == "Test Deposition"
    assert response.get_json()["metadata"]["description"] == "This is a test deposition created via Fakenodo API"

    deposition_id = response.get_json()["id"]

    upload_url = f"{FAKENODO_API_URL}/{deposition_id}/files"
    files = {"file": open(file_path, "rb")}

    response = test_client.post(upload_url, data=files)
    files["file"].close()

    file_body = response.get_json()
    assert response.status_code == 201
    assert "id" in file_body
    assert "filename" in file_body
    assert "checksum" in file_body
    assert "filesize" in file_body

    delete_url = f"{FAKENODO_API_URL}/{deposition_id}"
    response = test_client.delete(delete_url)

    assert response.status_code == 201
    cleanup(file_path)


def cleanup(file_path):
    """Helper function to remove the test file."""
    if os.path.exists(file_path):
        os.remove(file_path)
