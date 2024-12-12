from app.modules.auth.services import AuthenticationService
from app.modules.profile.services import UserProfileService
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
    logout(test_client)

    response = test_client.get("/profile/edit", follow_redirects=False)
    assert response.status_code == 302, "Unauthenticated users should be redirected."
    assert "/login" in response.headers["Location"], "Redirect should be to the login page."


def test_model_user_profile_save(test_client):
    """
    Tests the save method of the UserProfile model.
    """
    with test_client.application.app_context():
        user = User(email="save_test_user@example.com", password="password123")
        db.session.add(user)
        db.session.commit()

        profile = UserProfile(user_id=user.id, name="SaveTest", surname="User")
        profile.save()

        saved_profile = UserProfile.query.filter_by(user_id=user.id).first()
        assert saved_profile is not None, "UserProfile was not saved correctly."
        assert saved_profile.name == "SaveTest", "UserProfile name is incorrect."
        assert saved_profile.surname == "User", "UserProfile surname is incorrect."


def test_edit_profile_invalid_csrf_token(test_client):
    """
    Tests that an invalid CSRF token is handled correctly when editing a profile.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    response = test_client.get("/profile/edit")
    assert response.status_code == 200, "Failed to load edit profile page."

    csrf_token = "invalid_token"

    form_data = {
        "name": "CSRFTest",
        "surname": "Invalid",
        "orcid": "0000-0003-1825-0097",
        "affiliation": "Test Affiliation",
        "csrf_token": csrf_token,
    }
    response = test_client.post("/profile/edit", data=form_data, follow_redirects=False)
    assert response.status_code in [302, 400], "Expected a 302 redirect or 400 error for invalid CSRF token."

    logout(test_client)


def test_profile_routes_404(test_client):
    """
    Tests accessing non-existent routes in the profile blueprint.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    response = test_client.get("/profile/nonexistent_route", follow_redirects=False)
    assert response.status_code == 404, "Non-existent route should return a 404."

    logout(test_client)


def test_service_update_profile_invalid_id(test_client):
    """
    Tests the update_profile service method with an invalid user_profile_id.
    """
    with test_client.application.app_context():
        from app.modules.profile.forms import UserProfileForm
        
        service = UserProfileService()
        form_data = {
            "name": "Test",
            "surname": "Invalid",
            "orcid": "0000-0003-1825-0097",
            "affiliation": "Test Affiliation",
        }
        form = UserProfileForm(data=form_data)
        result, errors = service.update_profile(-1, form)

        assert result is None, "Expected no result for invalid profile ID."
        assert errors is not None, "Expected errors for invalid profile ID."
        assert "UserProfile with id -1 does not exist." in errors.get("error", ""), "Expected specific error message for invalid profile ID."


def test_service_update_profile_required_fields(test_client):
    """
    Tests the update_profile service method for required field validation errors.
    """
    with test_client.application.app_context():
        from app.modules.profile.forms import UserProfileForm

        invalid_form_data = {
            "name": "",
            "surname": "",
            "orcid": "0000-0000-0000-000X",
            "affiliation": "Valid Affiliation",
        }
        form = UserProfileForm(data=invalid_form_data)
        form.validate()

        assert "name" in form.errors, f"Expected 'name' error, got {form.errors}"
        assert "surname" in form.errors, f"Expected 'surname' error, got {form.errors}"
        assert "orcid" in form.errors, f"Expected 'orcid' error, got {form.errors}"
        assert "Invalid ORCID format" in form.errors["orcid"], f"Expected 'Invalid ORCID format' in 'orcid' errors, got {form.errors['orcid']}"
