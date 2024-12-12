import pytest
from app import db
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile
from app.modules.dataset.models import DataSet, DSMetaData, PublicationType
from app.modules.conftest import login, logout


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Sets up test_client with initial data for profile integration tests.
    """
    with test_client.application.app_context():
        user = User(email="testuser@example.com", password="test1234")
        db.session.add(user)
        db.session.commit()

        profile = UserProfile(user_id=user.id, name="Test", surname="User", orcid="0000-0002-1825-0097", affiliation="Test Affiliation")
        db.session.add(profile)
        db.session.commit()

        metadata = DSMetaData(
            title="Dataset 1",
            description="Test Dataset",
            publication_type=PublicationType.JOURNAL_ARTICLE
        )
        db.session.add(metadata)
        db.session.commit()

        dataset = DataSet(user_id=user.id, ds_meta_data_id=metadata.id)
        db.session.add(dataset)
        db.session.commit()

    yield test_client


def test_update_profile_invalid_method(test_client):
    """
    Tests that using an unsupported HTTP method returns a 405 error.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    response = test_client.put("/profile/edit", data={})
    assert response.status_code == 405, "PUT method should not be allowed for this route."

    logout(test_client)


def test_profile_summary_pagination(test_client):
    """
    Tests that the profile summary handles pagination correctly.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    response = test_client.get("/profile/summary?page=2")
    assert response.status_code == 200, "Failed to access profile summary with pagination."

    if b"No datasets uploaded" not in response.data:
        # Debugging message for datasets found
        datasets = db.session.query(DataSet).filter_by(user_id=1).offset(5).all()
        assert not datasets, f"Unexpected datasets found on page 2: {datasets}"

    logout(test_client)


def test_profile_summary_invalid_pagination(test_client):
    """
    Tests that the profile summary handles invalid page numbers gracefully.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    response = test_client.get("/profile/summary?page=invalid")
    assert response.status_code == 200, "Invalid pagination parameter should not cause a crash."
    assert b"User profile" in response.data, "Profile summary did not load with invalid pagination."

    logout(test_client)


def test_public_profile_access_denied_for_self(test_client):
    """
    Tests that users cannot access their own public profile via /public_profile/<user_id>.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    with test_client.application.app_context():
        user = User.query.filter_by(email="testuser@example.com").first()

    response = test_client.get(f"/public_profile/{user.id}")
    assert response.status_code == 403, "Users should not be able to access their own public profile."

    logout(test_client)


def test_view_profile_edit_redirects_unauthenticated(test_client):
    """
    Tests that unauthenticated users are redirected when attempting to access the edit profile page.
    """
    logout(test_client)  # Ensure no user is logged in.

    response = test_client.get("/profile/edit", follow_redirects=False)
    assert response.status_code == 302, "Unauthenticated users should be redirected."
    assert "/login" in response.headers["Location"], "Redirect should be to the login page."
