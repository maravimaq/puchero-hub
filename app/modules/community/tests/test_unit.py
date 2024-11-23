import pytest
from app import db
from app.modules.auth.models import User
from app.modules.community.models import Community
from app.modules.community.services import CommunityService

service = CommunityService()

@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Create users
        owner_user = User(email='owner@example.com', password='test1234')
        member_user = User(email='member@example.com', password='test1234')
        new_user = User(email='new_user@example.com', password='test1234')

        db.session.add(owner_user)
        db.session.add(member_user)
        db.session.add(new_user)
        db.session.commit()

        # Create a community
        community = Community(
            name="Test Community",
            description="A community for testing",
            owner_id=owner_user.id
        )
        community.members.append(owner_user)
        community.members.append(member_user)

        db.session.add(community)
        db.session.commit()

    yield test_client


def test_sample_assertion(test_client):
    """
    Sample test to verify that the test framework and environment are working correctly.
    It does not communicate with the Flask application; it only performs a simple assertion to
    confirm that the tests in this module can be executed.
    """
    greeting = "Hello, World!"
    assert greeting == "Hello, World!", "The greeting does not coincide with 'Hello, World!'"


def test_join_community(test_client):
    """
    Tests if a user can successfully join a community.
    """
    with test_client.application.app_context():
        new_user = User.query.filter_by(email='new_user@example.com').first()
        community = Community.query.filter_by(name="Test Community").first()

        result = service.join_community(community.id, new_user)
        community = Community.query.filter_by(name="Test Community").first()

        assert result, "The user failed to join the community."
        assert new_user in community.members, "The user did not successfully join the community."