import pytest
from app import db
from app.modules.conftest import login, logout
from app.modules.auth.models import User
from app.modules.dataset.models import DataSet, DSMetaData, PublicationType


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add specific test data.
    """
    with test_client.application.app_context():
        user = User(email='testuser@example.com', password='testpassword')
        db.session.add(user)
        db.session.commit()

        other_user = User(email='otheruser@example.com', password='otherpassword')
        db.session.add(other_user)
        db.session.commit()

        metadata1 = DSMetaData(
            title="Dataset 1 Metadata",
            description="Description for Dataset 1",
            publication_type=PublicationType.JOURNAL_ARTICLE
        )
        db.session.add(metadata1)
        db.session.commit()

        dataset1 = DataSet(user_id=other_user.id, ds_meta_data_id=metadata1.id)
        db.session.add(dataset1)
        db.session.commit()

    yield test_client


def test_view_user_datasets_success(test_client):
    """
    Tests successful access to the public profile datasets of another user.
    """
    login_response = login(test_client, "testuser@example.com", "testpassword")
    assert login_response.status_code == 200

    with test_client.application.app_context():
        other_user = User.query.filter_by(email='otheruser@example.com').first()
        other_user_id = other_user.id

    response = test_client.get(f"/public_profile/{other_user_id}")
    assert response.status_code == 200, "Failed to access the public profile of another user."
    assert b"Dataset 1 Metadata" in response.data, "Dataset details are not displayed."
    assert b"Journal Article" in response.data, "Dataset publication type is missing."
    logout(test_client)


def test_view_user_datasets_not_logged_in(test_client):
    """
    Tests that unauthenticated access redirects to the login page.
    """
    logout_response = test_client.get("/logout", follow_redirects=False)
    assert logout_response.status_code == 302

    response = test_client.get("/public_profile/1", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers.get("Location", "")


def test_view_user_datasets_invalid_user(test_client):
    """
    Tests accessing a profile for a nonexistent user.
    """
    login_response = login(test_client, "testuser@example.com", "testpassword")
    assert login_response.status_code == 200

    response = test_client.get("/public_profile/999")
    assert response.status_code == 404

    logout(test_client)


def test_view_user_datasets_html_structure(test_client):
    """
    Tests that the public profile page contains expected HTML structure.
    """
    login_response = login(test_client, "testuser@example.com", "testpassword")
    assert login_response.status_code == 200

    with test_client.application.app_context():
        other_user = User.query.filter_by(email="otheruser@example.com").first()

    response = test_client.get(f"/public_profile/{other_user.id}")
    assert response.status_code == 200, "Failed to access the public profile page."
    assert b"<table" in response.data, "Table structure is missing."
    assert b"<thead" in response.data, "Table headers are missing."
    assert b"<tbody" in response.data, "Table body is missing."
    assert b"<tr" in response.data, "Table rows are missing."
    logout(test_client)


def test_view_user_datasets_contains_correct_headers(test_client):
    """
    Verifies that the public profile page includes correct table headers for datasets.
    """
    login_response = login(test_client, "testuser@example.com", "testpassword")
    assert login_response.status_code == 200

    with test_client.application.app_context():
        other_user = User.query.filter_by(email="otheruser@example.com").first()
        other_user_id = other_user.id

    response = test_client.get(f"/public_profile/{other_user_id}")
    assert response.status_code == 200, "Failed to access the public profile page."
    assert b"<th>Title</th>" in response.data, "Title header is missing."
    assert b"<th>Publication type</th>" in response.data, "Publication type header is missing."

    logout(test_client)
