import pytest
from app.modules.fakenodo.services import FakenodoService

@pytest.fixture(scope="module")
def fakenodo_service():
    """
    Fixture to initialize the FakenodoService instance for testing.
    """
    return FakenodoService()


def test_test_connection(fakenodo_service):
    """
    Test if the connection test works correctly.
    """
    result = fakenodo_service.test_connection()
    assert result is True, "Connection test failed."

def test_create_new_deposition(fakenodo_service):
    """
    Test creating a new deposition.
    """
    metadata = {"title": "Sample Deposition", "description": "This is a test deposition."}
    deposition = fakenodo_service.create_new_deposition(metadata)

    assert deposition["id"] == 1, "Deposition ID mismatch."
    assert deposition["title"] == "Sample Deposition", "Deposition title mismatch."
    assert deposition["description"] == "This is a test deposition.", "Deposition description mismatch."
    assert deposition["status"] == "draft", "Deposition status mismatch."

def test_get_all_depositions(fakenodo_service):
    """
    Test retrieving all depositions.
    """
    all_depositions = fakenodo_service.get_all_depositions()

    assert "depositions" in all_depositions, "Depositions list is missing."
    assert len(all_depositions["depositions"]) > 0, "No depositions were retrieved."
    assert all_depositions["depositions"][0]["title"] == "Sample Deposition", "Depositions data mismatch."


def test_upload_file(fakenodo_service):
    """
    Test uploading a file to a deposition.
    """
    deposition_id = 1
    file_data = {"filename": "example.txt", "content": "Sample content."}
    file_info = fakenodo_service.upload_file(deposition_id, file_data)

    assert file_info["filename"] == "example.txt", "File name mismatch."
    assert file_info["status"] == "uploaded", "File upload status mismatch."

def test_publish_deposition(fakenodo_service):
    """
    Test publishing a deposition.
    """
    deposition_id = 1
    published_deposition = fakenodo_service.publish_deposition(deposition_id)

    assert published_deposition["id"] == deposition_id, "Deposition ID mismatch."
    assert published_deposition["status"] == "published", "Deposition status mismatch after publishing."


def test_get_deposition(fakenodo_service):
    """
    Test retrieving a single deposition by ID.
    """
    deposition_id = 1
    deposition = fakenodo_service.get_deposition(deposition_id)

    assert deposition["id"] == deposition_id, "Deposition ID mismatch."
    assert deposition["title"] == "Sample Deposition", "Deposition title mismatch."


def test_delete_deposition(fakenodo_service):
    """
    Test deleting a deposition.
    """
    deposition_id = 1
    delete_response = fakenodo_service.delete_deposition(deposition_id)

    assert delete_response["id"] == deposition_id, "Deleted deposition ID mismatch."
    assert delete_response["status"] == "deleted", "Deletion status mismatch."

    with pytest.raises(Exception, match="Deposition not found"):
        fakenodo_service.get_deposition(deposition_id)


def test_get_doi(fakenodo_service):
    """
    Test retrieving a DOI for a deposition.
    """
    deposition_id = 2
    
    fakenodo_service.create_new_deposition({"title": "Second Deposition", "description": "Another test."})

    doi = fakenodo_service.get_doi(deposition_id)
    assert doi == f"10.1234/fake-doi-{deposition_id}", "DOI generation mismatch."