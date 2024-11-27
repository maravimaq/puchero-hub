import pytest

from app import db
from app.modules.auth.models import User
from app.modules.community.models import Community
from app.modules.profile.models import UserProfile
from app.modules.conftest import login, logout
from unittest.mock import patch


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        user_test = User(email='testuser@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Test", surname="User")
        db.session.add(profile)
        db.session.commit()

        community1 = Community(name='Community Test 1',
                               description='Description for Community 1', owner_id=user_test.id)
        community2 = Community(name='Community Test 2',
                               description='Description for Community 2', owner_id=user_test.id)
        db.session.add(community1)
        db.session.add(community2)

        user_test2 = User(email='testuser2@example.com', password='test1234')
        db.session.add(user_test2)
        db.session.commit()

        profile2 = UserProfile(user_id=user_test2.id, name="Second", surname="User")
        db.session.add(profile2)

        joinable_community = Community(name='Joinable Community',
                                       description='Community for testing join', owner_id=user_test.id)
        db.session.add(joinable_community)

        db.session.commit()

    yield test_client


def get_community_by_name(name, test_client):
    """
    Helper function to retrieve a community by name.
    """
    with test_client.application.app_context():
        return Community.query.filter_by(name=name).first()


def test_create_community(test_client):
    """
    Test creating a community via POST request.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.post('/community/create', data={
        'name': 'Test Community',
        'description': 'This is a test community description.'
    }, follow_redirects=True)
    assert response.status_code == 200

    community = get_community_by_name('Test Community', test_client)
    assert community is not None, "Community was not found in the database."

    logout(test_client)


def test_create_community_error_handling(test_client):
    """
    Test error handling when an exception occurs during community creation.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    with patch("app.db.session.add", side_effect=Exception("Simulated Database Error")):
        response = test_client.post('/community/create', data={
            'name': 'Faulty Community',
            'description': 'This should fail due to a simulated error.'
        }, follow_redirects=True)

    assert response.status_code == 200, "Error handling did not return a proper response."
    assert b"Error creating community" in response.data, "Error message not displayed to the user."
    assert b"Simulated Database Error" in response.data, "Exception details not included in the flash message."

    logout(test_client)


def test_edit_community(test_client):
    login(test_client, "testuser@example.com", "test1234")

    with test_client.application.app_context():
        community = Community.query.filter_by(name='Community Test 1').first()
        assert community, "Community Test 1 not found."

    response = test_client.post(f'/community/edit/{community.id}', data={
        'name': 'Edited Community',
        'description': 'Updated description.'
    }, follow_redirects=True)
    assert response.status_code == 200

    with test_client.application.app_context():
        updated_community = Community.query.get(community.id)
        assert updated_community.name == 'Edited Community'
        assert updated_community.description == 'Updated description.'

    logout(test_client)


def test_edit_nonexistent_or_unauthorized_community(test_client):
    """
    Test editing a nonexistent or unauthorized community.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get('/community/edit/99999', follow_redirects=True)
    assert response.status_code == 200, "Redirection failed."
    assert b"Community not found or you do not have permission to edit it." in response.data, \
        "Error message for nonexistent community not displayed."

    with test_client.application.app_context():
        user = User.query.filter_by(email="testuser2@example.com").first()
        community = Community(name="Other User's Community", description="Test", owner_id=user.id)
        db.session.add(community)
        db.session.commit()

    response = test_client.get(f'/community/edit/{community.id}', follow_redirects=True)
    assert response.status_code == 200, "Redirection failed."
    assert b"Community not found or you do not have permission to edit it." in response.data, \
        "Error message for unauthorized access not displayed."

    logout(test_client)


def test_edit_community_update_failure(test_client):
    """
    Test handling a failure when updating a community.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    with test_client.application.app_context():
        community = Community(name="Editable Community", description="Original Description", owner_id=1)
        db.session.add(community)
        db.session.commit()

    with test_client.application.app_context():
        community = Community.query.filter_by(name="Editable Community").first()

    with patch("app.modules.community.services.CommunityService.update", return_value=None):
        response = test_client.post(f'/community/edit/{community.id}', data={
            'name': 'Updated Community',
            'description': 'Updated Description'
        }, follow_redirects=True)

    assert response.status_code == 200, "Redirection failed."
    assert b"Error updating community. Please try again." in response.data, \
        "Error message for update failure not displayed."

    logout(test_client)


def test_delete_community(test_client):
    login(test_client, "testuser@example.com", "test1234")

    with test_client.application.app_context():
        community = Community.query.filter_by(name='Community Test 2').first()
        assert community, "Community Test 2 not found."

    response = test_client.post(f'/community/delete/{community.id}', follow_redirects=True)
    assert response.status_code == 200

    with test_client.application.app_context():
        deleted_community = Community.query.get(community.id)
        assert deleted_community is None

    logout(test_client)


def test_delete_nonexistent_or_unauthorized_community(test_client):
    """
    Test deleting a nonexistent or unauthorized community.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.post('/community/delete/99999', follow_redirects=True)
    assert response.status_code == 200, "Redirection failed."
    assert b"Community not found or you do not have permission to delete it." in response.data, \
        "Error message for nonexistent community not displayed."

    with test_client.application.app_context():
        user = User.query.filter_by(email="testuser2@example.com").first()
        community = Community(name="Other User's Community", description="Test", owner_id=user.id)
        db.session.add(community)
        db.session.commit()

    response = test_client.post(f'/community/delete/{community.id}', follow_redirects=True)
    assert response.status_code == 200, "Redirection failed."
    assert b"Community not found or you do not have permission to delete it." in response.data, \
        "Error message for unauthorized access not displayed."

    logout(test_client)


def test_delete_community_failure(test_client):
    """
    Test handling a failure when deleting a community.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    with test_client.application.app_context():
        community = Community(name="Deletable Community", description="Test", owner_id=1)
        db.session.add(community)
        db.session.commit()

    with test_client.application.app_context():
        community = Community.query.filter_by(name="Deletable Community").first()

    with patch("app.modules.community.services.CommunityService.delete", 
               side_effect=Exception("Simulated Delete Error")):
        response = test_client.post(f'/community/delete/{community.id}', follow_redirects=True)

    assert response.status_code == 200, "Redirection failed."
    assert b"Error deleting community" in response.data, "Error message for delete failure not displayed."

    logout(test_client)


def test_list_communities_not_joined(test_client):
    """
    Test listing communities not joined by the user and joining one.
    """
    login_response = login(test_client, "testuser2@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get('/communities/not-joined', follow_redirects=True)
    assert response.status_code == 200, "Could not access the 'not joined' communities page."
    assert b"Joinable Community" in response.data, "Joinable Community should be listed as not joined."

    community = get_community_by_name('Joinable Community', test_client)
    response = test_client.post(f'/community/join/{community.id}', follow_redirects=True)
    assert response.status_code == 200, "Could not join the community."

    response = test_client.get('/communities/not-joined', follow_redirects=True)
    assert response.status_code == 200
    assert b"Joinable Community" not in response.data, "Joined community still appears in 'not joined' list."

    logout(test_client)


def test_join_community(test_client):
    login(test_client, "testuser2@example.com", "test1234")

    with test_client.application.app_context():
        community = Community.query.filter_by(name='Joinable Community').first()
        assert community, "Joinable Community not found."

    response = test_client.post(f'/community/join/{community.id}', follow_redirects=True)
    assert response.status_code == 200

    with test_client.application.app_context():
        community = Community.query.get(community.id)
        user = User.query.filter_by(email='testuser2@example.com').first()
        assert user in community.members

    logout(test_client)


def test_list_not_joined_communities(test_client):
    login(test_client, "testuser2@example.com", "test1234")

    response = test_client.get('/communities/not-joined', follow_redirects=True)
    assert response.status_code == 200
    assert b"Communities You Haven't Joined" in response.data

    logout(test_client)


def test_view_community_details(test_client):
    """
    Test viewing the details of a community.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.post('/community/create', data={
        'name': 'Test Community for Details',
        'description': 'Description for Test Community Details'
    }, follow_redirects=True)
    assert response.status_code == 200, "Community creation failed."

    community = get_community_by_name('Test Community for Details', test_client)
    assert community is not None, "Test Community for Details was not found in the database."

    response = test_client.get(f'/community/{community.id}', follow_redirects=True)
    assert response.status_code == 200, "Could not access the community details page."
    assert b"Test Community for Details" in response.data, "Community name not found on details page."
    assert (
        b"Description for Test Community Details" in response.data
        ), "Community description not found on details page."

    logout(test_client)


def test_show_nonexistent_community(test_client):
    """
    Test showing a nonexistent community.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get('/community/99999', follow_redirects=True)

    assert response.status_code == 200, "Redirection failed."

    with test_client.session_transaction() as session:
        flashed_messages = session['_flashes']
        assert any("Community not found." in msg[1] for msg in flashed_messages), \
            "Message 'Community not found.' was not flashed."

    logout(test_client)
