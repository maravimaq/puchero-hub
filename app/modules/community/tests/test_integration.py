import pytest

from app import db
from app.modules.auth.models import User
from app.modules.community.models import Community
from app.modules.profile.models import UserProfile
from app.modules.conftest import login, logout


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Crear usuario principal de prueba
        user_test = User(email='testuser@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        # Crear perfil para el usuario principal
        profile = UserProfile(user_id=user_test.id, name="Test", surname="User")
        db.session.add(profile)
        db.session.commit()

        # Crear un par de comunidades para el usuario principal
        community1 = Community(name='Community Test 1',
                               description='Description for Community 1', owner_id=user_test.id)
        community2 = Community(name='Community Test 2',
                               description='Description for Community 2', owner_id=user_test.id)
        db.session.add(community1)
        db.session.add(community2)

        # Crear un segundo usuario sin comunidades
        user_test2 = User(email='testuser2@example.com', password='test1234')
        db.session.add(user_test2)
        db.session.commit()

        profile2 = UserProfile(user_id=user_test2.id, name="Second", surname="User")
        db.session.add(profile2)

        # Crear una comunidad para que el segundo usuario pueda unirse
        joinable_community = Community(name='Joinable Community',
                                       description='Community for testing join', owner_id=user_test.id)
        db.session.add(joinable_community)

        # Confirmar los cambios
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

    # Crear comunidad
    response = test_client.post('/community/create', data={
        'name': 'Test Community',
        'description': 'This is a test community description.'
    }, follow_redirects=True)
    assert response.status_code == 200

    # Verificar que la comunidad fue creada
    community = get_community_by_name('Test Community', test_client)
    assert community is not None, "Community was not found in the database."

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
    # Log in as the test user
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    # Create a community via POST request
    response = test_client.post('/community/create', data={
        'name': 'Test Community for Details',
        'description': 'Description for Test Community Details'
    }, follow_redirects=True)
    assert response.status_code == 200, "Community creation failed."

    # Fetch the newly created community from the database
    community = get_community_by_name('Test Community for Details', test_client)
    assert community is not None, "Test Community for Details was not found in the database."

    # Access the community details page
    response = test_client.get(f'/community/{community.id}', follow_redirects=True)
    assert response.status_code == 200, "Could not access the community details page."
    assert b"Test Community for Details" in response.data, "Community name not found on details page."
    assert (
        b"Description for Test Community Details" in response.data
        ), "Community description not found on details page."

    # Log out
    logout(test_client)
