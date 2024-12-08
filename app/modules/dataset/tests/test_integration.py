import pytest
import os
from app import db
from app.modules.auth.models import User
from app.modules.dataset.models import DataSet, DSMetaData, PublicationType
from app.modules.profile.models import UserProfile
from app.modules.conftest import login, logout
from werkzeug.datastructures import FileStorage


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extend the test_client fixture to add specific data for dataset testing.
    """
    with test_client.application.app_context():
        user = User(email="testuser@example.com", password="test1234")
        db.session.add(user)
        db.session.commit()

        # Create a profile for the test user
        profile = UserProfile(user_id=user.id, name="Test", surname="User")
        db.session.add(profile)
        db.session.commit()

        # Use PublicationType enum for valid publication_type values
        ds_meta1 = DSMetaData(
            title="Test Dataset 1",
            description="First test dataset.",
            publication_type=PublicationType.JOURNAL_ARTICLE,  # Use enum value
            publication_doi="10.1234/test1",
        )
        ds_meta2 = DSMetaData(
            title="Test Dataset 2",
            description="Second test dataset.",
            publication_type=PublicationType.BOOK,  # Use another valid enum value
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
    # Login as the test user
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    # Define paths for the source and destination directories
    user_temp_folder = "uploads/temp/2"
    dataset_folder = "/app/uploads/user_2/dataset_3"
    os.makedirs(user_temp_folder, exist_ok=True)

    # Clean up destination folder to avoid conflicts
    if os.path.exists(dataset_folder):
        for file in os.listdir(dataset_folder):
            os.remove(os.path.join(dataset_folder, file))
        os.rmdir(dataset_folder)

    # Create the temporary file in the correct location
    temp_file_path = os.path.join(user_temp_folder, "test_model.uvl")
    with open(temp_file_path, "w") as temp_file:
        temp_file.write("This is a test UVL file.")

    # Prepare POST data, using just the filename
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

    # Post data to create the dataset
    response = test_client.post('/dataset/upload', data=data, follow_redirects=True)

    # Assertions
    assert response.status_code == 200, "Dataset creation failed."
    assert b"Everything works!" in response.data, "Success message not found."

    # Clean up test directories and files if they still exist
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
    if os.path.exists(user_temp_folder):
        os.rmdir(user_temp_folder)
    if os.path.exists(dataset_folder):
        for file in os.listdir(dataset_folder):
            os.remove(os.path.join(dataset_folder, file))
        os.rmdir(dataset_folder)

    # Logout after the test
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

'''
def test_edit_dataset(test_client):
    """
    Test editing an existing dataset.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    dataset = get_dataset_by_title("Test Dataset 1", test_client)
    assert dataset is not None, "Dataset not found in the database."

    response = test_client.post(f'/dataset/edit/{dataset.id}', data={
        'title': 'Edited Dataset Title',
        'desc': 'Updated description.',
        'tags': 'edited, dataset',
    }, follow_redirects=True)

    assert response.status_code == 200, "Dataset edit failed."

    with test_client.application.app_context():
        updated_dataset = DSMetaData.query.get(dataset.id)
        assert updated_dataset.title == "Edited Dataset Title"
        assert updated_dataset.description == "Updated description."

    logout(test_client)


def test_delete_dataset(test_client):
    """
    Test deleting a dataset.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    dataset = get_dataset_by_title("Test Dataset 2", test_client)
    assert dataset is not None, "Dataset not found in the database."

    response = test_client.post(f'/dataset/delete/{dataset.id}', follow_redirects=True)
    assert response.status_code == 200, "Dataset delete failed."

    with test_client.application.app_context():
        deleted_dataset = DataSet.query.get(dataset.id)
        assert deleted_dataset is None, "Dataset still exists in the database."

    logout(test_client)


def test_view_dataset_details(test_client):
    """
    Test viewing the details of a dataset.
    """
    login_response = login(test_client, "testuser@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    dataset = get_dataset_by_title("Test Dataset 1", test_client)
    assert dataset is not None, "Dataset not found in the database."

    response = test_client.get(f'/dataset/view/{dataset.id}', follow_redirects=True)
    assert response.status_code == 200, "Dataset details page not accessible."
    assert b"Test Dataset 1" in response.data
    assert b"First test dataset." in response.data

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
'''