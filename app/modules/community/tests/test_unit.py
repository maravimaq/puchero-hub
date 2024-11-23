import pytest
from app import db
from app.modules.auth.models import User
from app.modules.community.models import Community
from app.modules.community.services import CommunityService
from app.modules.dataset.models import DSMetaData, DataSet, PublicationType
from datetime import datetime


service = CommunityService()


@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Crear usuarios
        owner_user = User(email='owner@example.com', password='test1234')
        member_user = User(email='member@example.com', password='test1234')
        new_user = User(email='new_user@example.com', password='test1234')

        db.session.add(owner_user)
        db.session.add(member_user)
        db.session.add(new_user)
        db.session.commit()

        # Crear metadatos del dataset
        ds_meta_data = DSMetaData(
            title="Test Dataset",
            description="Dataset description for testing",
            publication_type=PublicationType.OTHER,
            publication_doi=None,
            dataset_doi=None,
            tags="test,dataset"
        )
        db.session.add(ds_meta_data)
        db.session.commit()

        # Crear una comunidad
        community = Community(
            name="Test Community",
            description="A community for testing",
            owner_id=owner_user.id
        )
        community.members.append(owner_user)
        community.members.append(member_user)
        db.session.add(community)
        db.session.commit()

        # Asociar un dataset con la comunidad
        dataset = DataSet(
            user_id=owner_user.id,
            community_id=community.id,
            ds_meta_data_id=ds_meta_data.id,
            created_at=datetime.utcnow()
        )
        db.session.add(dataset)
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


def test_create_community_service(test_client):
    """
    Test if the CommunityService correctly creates a community.
    """
    with test_client.application.app_context():
        owner_user = User.query.filter_by(email='owner@example.com').first()
        assert owner_user is not None, "Owner user should already exist."

        new_community_name = "Another Test Community"

        created_community = service.create(
            name=new_community_name,
            description="Another community for testing",
            owner_id=owner_user.id
        )

        assert created_community is not None, "The community should have been created."
        assert created_community.name == new_community_name, "The community name does not match."
        assert created_community.owner_id == owner_user.id, "The owner ID does not match."


def test_create_community_with_duplicate_name(test_client):
    """
    Test that creating a community with a duplicate name fails.
    """
    with test_client.application.app_context():
        user = User.query.filter_by(email='owner@example.com').first()
        duplicate_community = Community(
            name="Test Community",
            description="This should fail",
            owner_id=user.id
        )
        db.session.add(duplicate_community)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

        duplicate_community_in_db = Community.query.filter_by(description="This should fail").first()
        assert duplicate_community_in_db is None, "The duplicate community was incorrectly created."


def test_edit_community_as_owner(test_client):
    """
    Test if the owner can edit a community successfully.
    """
    with test_client.application.app_context():
        User.query.filter_by(email='owner@example.com').first()
        community = Community.query.filter_by(name="Test Community").first()

        community.name = "Edited Community Name"
        community.description = "Updated description"
        db.session.commit()

        edited_community = Community.query.filter_by(id=community.id).first()
        assert edited_community.name == "Edited Community Name", "The community name was not updated."
        assert edited_community.description == "Updated description", "The community description was not updated."


def test_delete_community_as_owner(test_client):
    """
    Test if the owner can delete a community successfully.
    """
    with test_client.application.app_context():
        owner_user = User(email='delete_owner@example.com', password='test1234')
        db.session.add(owner_user)
        db.session.commit()

        community = Community(
            name="Community to Delete",
            description="This community will be deleted in the test",
            owner_id=owner_user.id
        )
        community.members.append(owner_user)

        db.session.add(community)
        db.session.commit()

        community_id = community.id

        db.session.delete(community)
        db.session.commit()

        deleted_community = Community.query.filter_by(id=community_id).first()
        assert deleted_community is None, "The community was not deleted successfully."


def create_community(name, description, owner_user):
    community = Community(name=name, description=description, owner_id=owner_user.id)
    community.members.append(owner_user)
    db.session.add(community)
    db.session.commit()
    return community


def create_ds_meta_data(title, description, publication_type):
    ds_meta_data = DSMetaData(
        title=title,
        description=description,
        publication_type=publication_type,
        publication_doi=None,
        dataset_doi=None,
        tags="test,dataset"
    )
    db.session.add(ds_meta_data)
    db.session.commit()
    return ds_meta_data


def create_dataset(user, community, ds_meta_data):
    dataset = DataSet(
        user_id=user.id,
        community_id=community.id,
        ds_meta_data_id=ds_meta_data.id,
        created_at=datetime.utcnow()
    )
    db.session.add(dataset)
    db.session.commit()
    return dataset


def test_show_community_with_datasets(test_client):
    """
    Test if datasets are correctly shown in a community view.
    """
    with test_client.application.app_context():
        owner_user = User.query.filter_by(email="owner@example.com").first()
        assert owner_user is not None, "The owner user was not created correctly in the fixture."

        community = create_community("Dataset Test Community", "Community with a dataset for testing", owner_user)
        ds_meta_data = create_ds_meta_data("Test Dataset", "Dataset description for testing", PublicationType.OTHER)
        create_dataset(owner_user, community, ds_meta_data)

        community = service.get_with_datasets_by_id(community.id)  # Devuelve un objeto Community
        assert community is not None, "The test community was not retrieved correctly."
        assert isinstance(community, Community), "The result should be a Community object."

        datasets = community.datasets
        assert datasets is not None, "Datasets were not retrieved correctly."
        assert isinstance(datasets, list), "Datasets should be returned as a list."
        assert len(datasets) == 1, "The community should have exactly one dataset."
        assert datasets[0].ds_meta_data.title == "Test Dataset", "The dataset title does not match."
