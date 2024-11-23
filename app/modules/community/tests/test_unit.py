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

def test_get_all_communities_by_user(test_client):
    """
    Tests if all communities owned by a user are correctly retrieved.
    """
    with test_client.application.app_context():
        owner_user = User.query.filter_by(email='owner@example.com').first()

        communities = service.get_all_by_user(owner_user.id)

        assert len(communities) == 1, "The user should own exactly one community."
        assert communities[0].name == "Test Community", "The community name does not match."


def test_get_all_joined_communities_by_user(test_client):
    """
    Tests if all communities a user has joined are correctly retrieved.
    """
    with test_client.application.app_context():
        member_user = User.query.filter_by(email='member@example.com').first()

        joined_communities = service.get_all_joined_by_user(member_user.id)

        assert len(joined_communities) == 1, "The user should have joined exactly one community."
        assert joined_communities[0].name == "Test Community", "The joined community name does not match."


def test_get_members_by_community_id(test_client):
    """
    Tests if all members of a community are correctly retrieved by community ID.
    """
    with test_client.application.app_context():
        community = Community.query.filter_by(name="Test Community").first()

        community_with_members = service.get_members_by_id(community.id)

        members = community_with_members.members

        assert len(members) == 3, "The community should have exactly three members."
        member_emails = [member.email for member in members]
        assert 'owner@example.com' in member_emails, "Owner is missing in the members list."
        assert 'member@example.com' in member_emails, "Member is missing in the members list."
        assert 'new_user@example.com' in member_emails, "New user is missing in the members list."


def test_get_communities_not_joined_by_user(test_client):
    """
    Tests if all communities not joined by a user are correctly retrieved.
    """
    with test_client.application.app_context():
        new_user = User.query.filter_by(email='new_user@example.com').first()

        communities_not_joined = service.get_communities_not_joined_by_user(new_user.id)

        assert len(communities_not_joined) == 0, "The new user should have joined all available communities."


def test_user_cannot_join_community_twice(test_client):
    """
    Tests that a user cannot join the same community more than once.
    """
    with test_client.application.app_context():
        new_user = User.query.filter_by(email='new_user@example.com').first()
        community = Community.query.filter_by(name="Test Community").first()

        # Try joining the same community again
        result = service.join_community(community.id, new_user)

        assert not result, "The user should not be able to join the same community twice."
        assert community.members.count(new_user) == 1, "The user appears in the community members list more than once."


def test_get_all_owned_communities(test_client):
    """
    Tests if all communities owned by a user are correctly retrieved.
    """
    with test_client.application.app_context():
        owner_user = User.query.filter_by(email='owner@example.com').first()

        owned_communities = service.get_all_by_user(owner_user.id)

        assert len(owned_communities) == 1, "The owner should have exactly one owned community."
        assert owned_communities[0].name == "Test Community", "The community name does not match the owned community."


def test_join_nonexistent_community(test_client):
    """
    Tests that a user cannot join a community that does not exist.
    """
    with test_client.application.app_context():
        new_user = User.query.filter_by(email='new_user@example.com').first()

        nonexistent_community_id = 99999  # A community ID that doesn't exist
        result = service.join_community(nonexistent_community_id, new_user)

        assert not result, "The user should not be able to join a nonexistent community."


def test_get_all_joined_communities_for_nonexistent_user(test_client):
    """
    Tests if querying joined communities for a nonexistent user returns an empty list.
    """
    with test_client.application.app_context():
        nonexistent_user_id = 99999  # A user ID that doesn't exist

        joined_communities = service.get_all_joined_by_user(nonexistent_user_id)

        assert len(joined_communities) == 0, "Nonexistent user should not have joined any communities."


def test_get_members_by_nonexistent_community_id(test_client):
    """
    Tests if querying members for a nonexistent community returns an empty list.
    """
    with test_client.application.app_context():
        nonexistent_community_id = 99999  # A community ID that doesn't exist

        members = service.get_members_by_id(nonexistent_community_id)

        assert members is None, "Nonexistent community should not have any members."
