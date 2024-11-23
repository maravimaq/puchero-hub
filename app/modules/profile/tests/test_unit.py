import pytest

from app import db
from app.modules.conftest import login, logout
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    for module testing (por example, new users)
    """
    with test_client.application.app_context():
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

    yield test_client


def test_edit_profile_page_get(test_client):
    """
    Tests access to the profile editing page via a GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/profile/edit")
    assert response.status_code == 200, "The profile editing page could not be accessed."
    assert b"Edit profile" in response.data, "The expected content is not present on the page"

    logout(test_client)

def test_view_other_user_profile(test_client):
    """
    Tests accessing another user's profile page.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    # Create another user and their profile
    other_user = User(email="other_user@example.com", password="password123")
    db.session.add(other_user)
    db.session.commit()

    other_profile = UserProfile(user_id=other_user.id, name="Other", surname="User")
    db.session.add(other_profile)
    db.session.commit()

    # Access the other user's profile
    response = test_client.get(f"/public_profile/{other_user.id}")
    assert response.status_code == 200, "Error accessing the other user's profile."
    assert b"Other User" in response.data, "The profile data is not displayed correctly."

    logout(test_client)

def test_view_nonexistent_profile(test_client):
    """
    Tests that accessing a nonexistent user's profile returns a 404 error.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    nonexistent_user_id = 1000000  # A user ID that doesn't exist in the database
    response = test_client.get(f"/public_profile/{nonexistent_user_id}")
    assert response.status_code == 404, "Expected a 404 error for a nonexistent profile."

    logout(test_client)

def test_view_profile_unauthenticated(test_client):
    """
    Tests that an unauthenticated user cannot access a profile.
    """
    # Create another user and fetch the ID inside the app context
    with test_client.application.app_context():
        other_user = User(email="unauth_user@example.com", password="password123")
        db.session.add(other_user)
        db.session.commit()
        user_id = other_user.id  # Extract and store the ID inside the context

    # Attempt to access the profile without logging in
    response = test_client.get(f"/public_profile/{user_id}", follow_redirects=False)
    assert response.status_code == 302, "Unauthenticated access should redirect."
    assert "/login" in response.headers["Location"], "Unauthenticated access should redirect to the login page."

def test_view_profile_invalid_page(test_client):
    """
    Tests viewing a profile with an invalid page parameter.
    """
    # Login with the test user
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    # Create another user and their profile
    with test_client.application.app_context():
        other_user = User(email="other_user14@example.com", password="password123")
        db.session.add(other_user)
        db.session.commit()

        other_profile = UserProfile(user_id=other_user.id, name="Tortilla", surname="User")
        db.session.add(other_profile)
        db.session.commit()

    # Make a request to the profile summary with an invalid page number
    response = test_client.get(f"/profile/summary?page=invalid")
    assert response.status_code == 200, "Invalid page parameter should not crash the app."
    assert b"User profile" in response.data, "The profile page is not rendering as expected with invalid pagination."
    logout(test_client)
'''
def test_update_profile_success(test_client):
    """
    Tests successful profile update with valid data.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    # Fetch the user's profile
    with test_client.application.app_context():
        user = User.query.filter_by(email="user@example.com").first()
        profile = user.profile

    # Submit a POST request with updated profile data
    form_data = {
        "name": "UpdatedName",
        "surname": "UpdatedSurname",
        "orcid": "0000-0002-1825-0097",
        "affiliation": "Updated Affiliation",
    }
    response = test_client.post(f"/profile/edit", data=form_data, follow_redirects=True)
    assert response.status_code == 200, "Profile update failed."

    # Verify the updates in the database
    with test_client.application.app_context():
        updated_profile = UserProfile.query.get(profile.id)
        assert updated_profile.name == "UpdatedName", "Name was not updated."
        assert updated_profile.surname == "UpdatedSurname", "Surname was not updated."
        assert updated_profile.orcid == "0000-0002-1825-0097", "ORCID was not updated."
        assert updated_profile.affiliation == "Updated Affiliation", "Affiliation was not updated."

    logout(test_client)
'''
def test_view_profile_sensitive_data_not_exposed(test_client):
    """
    Tests that sensitive data (e.g., passwords) is not exposed in the profile response.
    """
    # Login with the test user
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    # Create another user and their profile
    with test_client.application.app_context():
        sensitive_user = User(email="sensitive_user@example.com", password="password123")
        db.session.add(sensitive_user)
        db.session.commit()

        sensitive_profile = UserProfile(
            user_id=sensitive_user.id, name="Sensitive", surname="Data"
        )
        db.session.add(sensitive_profile)
        db.session.commit()

    # Access the other user's profile summary (using a similar route to the provided test)
    response = test_client.get(f"/profile/summary")
    assert response.status_code == 200, "Error accessing the profile."

    # Verify that sensitive data like passwords and emails are not exposed in the response
    assert b"password123" not in response.data, "Sensitive password data exposed."
    assert b"sensitive_user@example.com" not in response.data, "Sensitive email exposed."

    logout(test_client)
