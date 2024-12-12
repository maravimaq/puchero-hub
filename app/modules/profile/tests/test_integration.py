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


