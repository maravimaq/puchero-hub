from unittest.mock import patch
import pytest
from app import db
from app.modules.auth.models import User
from app.modules.dataset.models import DataSet, DSMetaData, PublicationType
from app.modules.dataset.services import DataSetService

dataset_service = DataSetService()


@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():

        user = User(email="test_user@example.com", password="password123")
        db.session.add(user)
        db.session.commit()

        metadata1 = DSMetaData(
            title="Dataset 1",
            description="Description for Dataset 1",
            publication_type=PublicationType.JOURNAL_ARTICLE
        )
        metadata2 = DSMetaData(
            title="Dataset 2",
            description="Description for Dataset 2",
            publication_type=PublicationType.BOOK
        )
        db.session.add(metadata1)
        db.session.add(metadata2)
        db.session.commit()

        dataset1 = DataSet(user_id=user.id, ds_meta_data_id=metadata1.id)
        dataset2 = DataSet(user_id=user.id, ds_meta_data_id=metadata2.id)
        db.session.add(dataset1)
        db.session.add(dataset2)
        db.session.commit()

    yield test_client


def test_get_synchronized_dataset(test_client):
    """
    Tests if the get_synchronized method retrieves a synchronized dataset.
    """
    with test_client.application.app_context():

        user = User.query.filter_by(email="test_user@example.com").first()

        metadata = DSMetaData(
            title="Synchronized Dataset",
            description="This dataset is synchronized.",
            publication_type=PublicationType.JOURNAL_ARTICLE,
            dataset_doi="10.1234/synced.dataset"
        )
        db.session.add(metadata)
        db.session.commit()

        dataset = DataSet(
            user_id=user.id,
            ds_meta_data_id=metadata.id
        )
        db.session.add(dataset)
        db.session.commit()

        synchronized_datasets = dataset_service.get_synchronized(user.id)

        assert isinstance(synchronized_datasets, list), "The result should be a list."
        assert len(synchronized_datasets) > 0, "No synchronized datasets were found."

        first_dataset = synchronized_datasets[0]
        assert first_dataset.ds_meta_data.title == "Synchronized Dataset", "Dataset title mismatch."


def test_total_dataset_views(test_client):
    """
    Tests the total number of dataset views recorded.
    """
    with test_client.application.app_context():
        total_views = dataset_service.total_dataset_views()
        assert total_views == 0, "Expected zero views for all datasets."


def test_total_dataset_downloads(test_client):
    """
    Tests the total number of dataset downloads recorded.
    """
    with test_client.application.app_context():
        total_downloads = dataset_service.total_dataset_downloads()
        assert total_downloads == 0, "Expected zero downloads for all datasets."


def test_dataset_creation(test_client):
    """
    Tests the creation of a new dataset through the DataSetService.
    """
    with test_client.application.app_context():
        user = User(email="new_user@example.com", password="test1234")
        db.session.add(user)
        db.session.commit()

        metadata = DSMetaData(
            title="New Dataset",
            description="This is a new dataset.",
            publication_type=PublicationType.CONFERENCE_PAPER
        )
        db.session.add(metadata)
        db.session.commit()

        new_dataset = DataSet(user_id=user.id, ds_meta_data_id=metadata.id)
        db.session.add(new_dataset)
        db.session.commit()

        assert new_dataset.id is not None, "Failed to create a new dataset."
        assert new_dataset.ds_meta_data.title == "New Dataset", "Dataset title mismatch."


def test_pack_datasets_no_uploads_folder():
    service = DataSetService()
    with patch("os.path.exists", return_value=False):
        result = service.pack_datasets()
        assert result is None
