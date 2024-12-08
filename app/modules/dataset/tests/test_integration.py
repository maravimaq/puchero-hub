import pytest
import os
from app import db
from app.modules.auth.models import User
from app.modules.dataset.models import DataSet, DSMetaData, PublicationType
from app.modules.dataset.services import DataSetService
from app.modules.profile.models import UserProfile
from app.modules.conftest import login, logout


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extend the test_client fixture to add specific data for dataset testing.
    """
    with test_client.application.app_context():
        user = User(email="testuser@example.com", password="test1234")
        db.session.add(user)
        db.session.commit()

        profile = UserProfile(user_id=user.id, name="Test", surname="User")
        db.session.add(profile)
        db.session.commit()

        ds_meta1 = DSMetaData(
            title="Test Dataset 1",
            description="First test dataset.",
            publication_type=PublicationType.JOURNAL_ARTICLE,
            publication_doi="10.1234/test1",
        )
        ds_meta2 = DSMetaData(
            title="Test Dataset 2",
            description="Second test dataset.",
            publication_type=PublicationType.BOOK,
            publication_doi="10.1234/test2",
        )
        db.session.add_all([ds_meta1, ds_meta2])
        db.session.commit()

        dataset1 = DataSet(user_id=user.id, ds_meta_data_id=ds_meta1.id)
        dataset2 = DataSet(user_id=user.id, ds_meta_data_id=ds_meta2.id)
        db.session.add_all([dataset1, dataset2])
        db.session.commit()

    yield test_client


def get_dataset_by_title(title, test_client):
    """
    Helper function to retrieve a dataset by title.
    """
    with test_client.application.app_context():
        return DSMetaData.query.filter_by(title=title).first()


def test_create_dataset(test_client):
    """
    Test creating a dataset via POST request.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    user_temp_folder = "uploads/temp/2"
    dataset_folder = "/app/uploads/user_2/dataset_3"
    os.makedirs(user_temp_folder, exist_ok=True)

    if os.path.exists(dataset_folder):
        for file in os.listdir(dataset_folder):
            os.remove(os.path.join(dataset_folder, file))
        os.rmdir(dataset_folder)

    temp_file_path = os.path.join(user_temp_folder, "test_model.uvl")
    with open(temp_file_path, "w") as temp_file:
        temp_file.write("This is a test UVL file.")

    data = {
        'title': 'New Test Dataset',
        'desc': 'Description for new dataset.',
        'publication_type': PublicationType.JOURNAL_ARTICLE.value,
        'tags': 'test, dataset',
        'feature_models-0-uvl_filename': "test_model.uvl",
        'feature_models-0-title': 'Sample Feature Model',
        'feature_models-0-desc': 'Feature Model Description',
        'feature_models-0-publication_type': PublicationType.BOOK.value,
    }

    response = test_client.post('/dataset/upload', data=data, follow_redirects=True)

    assert response.status_code == 200, "Dataset creation failed."
    assert b"Everything works!" in response.data, "Success message not found."

    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
    if os.path.exists(user_temp_folder):
        os.rmdir(user_temp_folder)
    if os.path.exists(dataset_folder):
        for file in os.listdir(dataset_folder):
            os.remove(os.path.join(dataset_folder, file))
        os.rmdir(dataset_folder)

    logout(test_client)


def test_list_datasets(test_client):
    """
    Test listing datasets owned by the user.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    response = test_client.get('/dataset/list', follow_redirects=True)
    assert response.status_code == 200, "Could not load dataset list page."
    assert b"Test Dataset 1" in response.data
    assert b"Test Dataset 2" in response.data

    logout(test_client)


def test_edit_dataset(test_client):
    """
    Test editing an existing dataset.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    with test_client.application.app_context():
        dataset_service = DataSetService()

        user = User.query.filter_by(email="testuser@example.com").first()
        assert user is not None, "Test user not found in the database."

        dataset = DataSet.query.filter_by(user_id=user.id).first()
        assert dataset is not None, "Dataset not found in the database."

        updated_metadata = dataset_service.update_dsmetadata(
            dataset.ds_meta_data.id,
            title="Edited Dataset Title",
            description="Updated description",
            tags="edited, dataset",
        )

        assert updated_metadata.title == "Edited Dataset Title", "Title did not update."
        assert updated_metadata.description == "Updated description", "Description did not update."

    logout(test_client)

def test_delete_dataset(test_client):
    """
    Test deleting a dataset and its associated metadata.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    dataset_meta = get_dataset_by_title("Test Dataset 2", test_client)
    assert dataset_meta is not None, "Dataset metadata not found in the database."

    with test_client.application.app_context():
        dataset_service = DataSetService()

        dataset = DataSet.query.filter_by(ds_meta_data_id=dataset_meta.id).first()
        assert dataset is not None, "Dataset record not found for the metadata."

        dataset.delete()

        db.session.delete(dataset_meta)
        db.session.commit()

        deleted_dataset = DataSet.query.get(dataset.id)
        assert deleted_dataset is None, "Dataset still exists in the database."

        deleted_metadata = DSMetaData.query.get(dataset_meta.id)
        assert deleted_metadata is None, "Dataset metadata still exists in the database."

    logout(test_client)


def test_handle_nonexistent_dataset(test_client):
    """
    Test handling access to a nonexistent dataset.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    response = test_client.get('/dataset/view/99999', follow_redirects=True)
    assert response.status_code == 404, "Expected 404 for nonexistent dataset."

    logout(test_client)

def test_add_file_to_dataset(test_client):
    """
    Test adding a file to an existing dataset.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    with test_client.application.app_context():
        dataset_meta = get_dataset_by_title("Test Dataset 1", test_client)
        if dataset_meta is None:
            user = User.query.filter_by(email="testuser@example.com").first()
            dataset_meta = DSMetaData(
                title="Test Dataset 1",
                description="First test dataset.",
                publication_type=PublicationType.JOURNAL_ARTICLE
            )
            db.session.add(dataset_meta)
            db.session.commit()

            dataset = DataSet(user_id=user.id, ds_meta_data_id=dataset_meta.id)
            db.session.add(dataset)
            db.session.commit()

    temp_file_path = os.path.join("uploads/temp", "test_file.uvl")
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
    with open(temp_file_path, "w") as temp_file:
        temp_file.write("This is a test UVL file.")

    data = {'file': (open(temp_file_path, 'rb'), 'test_file.uvl')}
    response = test_client.post('/dataset/file/upload', data=data, content_type='multipart/form-data')

    assert response.status_code == 200, "Failed to upload file."
    assert b"UVL uploaded and validated successfully" in response.data, "Success message not found."

    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

    logout(test_client)
