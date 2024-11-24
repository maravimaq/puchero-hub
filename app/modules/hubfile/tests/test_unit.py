import pytest
from app import db
from app.modules.hubfile.models import Hubfile, HubfileDownloadRecord, HubfileViewRecord
from app.modules.featuremodel.models import FeatureModel, FMMetaData, FMMetrics
from app.modules.dataset.models import DataSet, DSMetaData
from app.modules.auth.models import User
from datetime import datetime


@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        db.session.query(HubfileDownloadRecord).delete()
        db.session.query(HubfileViewRecord).delete()
        db.session.query(Hubfile).delete()
        db.session.query(FeatureModel).delete()
        db.session.query(DataSet).delete()
        db.session.query(User).delete()
        db.session.commit()

        user = User(id=1, email="test@example.com", password="hashed_password")
        db.session.add(user)

        ds_metadata = DSMetaData(
            title="Sample Dataset",
            description="Dataset description",
            publication_type="REPORT",
            tags="sample,dataset",
            dataset_doi="10.1234/sample"
        )
        db.session.add(ds_metadata)
        db.session.commit()

        data_set = DataSet(
            user_id=user.id,
            ds_meta_data_id=ds_metadata.id,
            created_at=datetime.utcnow()
        )
        db.session.add(data_set)
        db.session.commit()

        fm_metrics = FMMetrics(solver="SAT Solver", not_solver="Non-SAT Solver")
        db.session.add(fm_metrics)
        db.session.commit()

        fm_metadata = FMMetaData(
            uvl_filename="sample_model.uvl",
            title="Sample Feature Model",
            description="Feature model description",
            publication_type="REPORT",
            uvl_version="1.0",
            fm_metrics=fm_metrics
        )
        db.session.add(fm_metadata)
        db.session.commit()

        feature_model = FeatureModel(
            data_set_id=data_set.id,
            fm_meta_data=fm_metadata
        )
        db.session.add(feature_model)
        db.session.commit()

        hubfile = Hubfile(
            name="test_file.uvl",
            checksum="checksum123",
            size=2048,
            feature_model_id=feature_model.id
        )
        db.session.add(hubfile)
        db.session.commit()

        view_record = HubfileViewRecord(
            user_id=user.id,
            file_id=hubfile.id,
            view_date=datetime.utcnow(),
            view_cookie="view_cookie"
        )
        db.session.add(view_record)

        download_record = HubfileDownloadRecord(
            user_id=user.id,
            file_id=hubfile.id,
            download_date=datetime.utcnow(),
            download_cookie="download_cookie"
        )
        db.session.add(download_record)
        db.session.commit()

    yield test_client

    with test_client.application.app_context():
        db.session.query(HubfileDownloadRecord).delete()
        db.session.query(HubfileViewRecord).delete()
        db.session.query(Hubfile).delete()
        db.session.query(FeatureModel).delete()
        db.session.query(DataSet).delete()
        db.session.query(User).delete()
        db.session.commit()



def test_sample_assertion(test_client):
    """
    Sample test to verify that the test framework and environment are working correctly.
    """
    greeting = "Hello, World!"
    assert greeting == "Hello, World!", "The greeting does not coincide with 'Hello, World!'"


def test_hubfile_creation(test_client):
    """
    Test if the Hubfile was created successfully in the test fixture.
    """
    with test_client.application.app_context():
        hubfile = Hubfile.query.first()
        assert hubfile is not None, "Hubfile should exist in the database."
        assert hubfile.name == "test_file.uvl", f"Expected name 'test_file.uvl', got {hubfile.name}."
        assert hubfile.size == 2048, f"Expected size 2048, got {hubfile.size}."


def test_hubfile_view_record(test_client):
    """
    Test if the Hubfile view record is created successfully.
    """
    with test_client.application.app_context():
        view_record = HubfileViewRecord.query.first()
        assert view_record is not None, "Hubfile view record should exist in the database."
        assert view_record.view_cookie == "view_cookie", \
            f"Expected view_cookie 'view_cookie', got {view_record.view_cookie}."


def test_hubfile_download_record(test_client):
    """
    Test if the Hubfile download record is created successfully.
    """
    with test_client.application.app_context():
        download_record = HubfileDownloadRecord.query.first()
        assert download_record is not None, "Hubfile download record should exist in the database."
        assert download_record.download_cookie == "download_cookie", \
            f"Expected download_cookie 'download_cookie', got {download_record.download_cookie}."


def test_hubfile_association_with_feature_model(test_client):
    """
    Test the association between Hubfile and FeatureModel.
    """
    with test_client.application.app_context():
        hubfile = Hubfile.query.first()
        assert hubfile is not None, "Hubfile should exist in the database."
        assert hubfile.feature_model_id is not None, "Hubfile should be associated with a FeatureModel."
        feature_model = FeatureModel.query.get(hubfile.feature_model_id)
        assert feature_model is not None, "FeatureModel associated with Hubfile should exist."
        assert feature_model.fm_meta_data.title == "Sample Feature Model", \
            f"Expected title 'Sample Feature Model', got {feature_model.fm_meta_data.title}."


def test_hubfile_formatted_size(test_client):
    """
    Test the get_formatted_size() method of Hubfile.
    """
    with test_client.application.app_context():
        hubfile = Hubfile.query.first()
        assert hubfile is not None, "Hubfile should exist in the database."
        formatted_size = hubfile.get_formatted_size()

        assert formatted_size.startswith("2") and formatted_size.endswith("KB"), \
            f"Expected formatted size starting with '2' and ending with 'KB', got '{formatted_size}'."


def test_hubfile_association_with_dataset(test_client):
    """
    Test the association between Hubfile and DataSet via FeatureModel.
    """
    with test_client.application.app_context():
        hubfile = Hubfile.query.first()
        assert hubfile is not None, "Hubfile should exist in the database."
        feature_model = FeatureModel.query.get(hubfile.feature_model_id)
        assert feature_model is not None, "FeatureModel associated with Hubfile should exist."
        dataset = DataSet.query.get(feature_model.data_set_id)
        assert dataset is not None, "DataSet associated with FeatureModel should exist."
        assert dataset.ds_meta_data.title == "Sample Dataset", \
            f"Expected dataset title 'Sample Dataset', got {dataset.ds_meta_data.title}."


def test_hubfile_to_dict(test_client):
    """
    Test the to_dict() method of Hubfile.
    """
    with test_client.application.app_context():
        hubfile = Hubfile.query.first()
        assert hubfile is not None, "Hubfile should exist in the database."

        with test_client.application.test_request_context('/'):
            hubfile_dict = hubfile.to_dict()

            assert hubfile_dict["id"] == hubfile.id, f"Expected id {hubfile.id}, got {hubfile_dict['id']}."
            assert hubfile_dict["name"] == hubfile.name, f"Expected name {hubfile.name}, got {hubfile_dict['name']}."
            assert hubfile_dict["url"] is not None, "Expected a URL key in the hubfile dictionary."
            assert hubfile_dict["size_in_bytes"] == hubfile.size, \
                f"Expected size_in_bytes {hubfile.size}, got {hubfile_dict['size_in_bytes']}."


def test_hubfile_deletion(test_client):
    """
    Test deleting a Hubfile and its associated records.
    """
    with test_client.application.app_context():
        hubfile = Hubfile.query.first()
        assert hubfile is not None, "Hubfile should exist before deletion."

        HubfileViewRecord.query.filter_by(file_id=hubfile.id).delete()
        HubfileDownloadRecord.query.filter_by(file_id=hubfile.id).delete()
        db.session.commit()

        db.session.delete(hubfile)
        db.session.commit()

        deleted_hubfile = Hubfile.query.get(hubfile.id)
        assert deleted_hubfile is None, "Hubfile should be deleted."

        view_record = HubfileViewRecord.query.filter_by(file_id=hubfile.id).first()
        download_record = HubfileDownloadRecord.query.filter_by(file_id=hubfile.id).first()
        assert view_record is None, "Associated HubfileViewRecord should be deleted."
        assert download_record is None, "Associated HubfileDownloadRecord should be deleted."


def test_hubfile_update(test_client):
    """
    Test updating an existing Hubfile's attributes.
    """
    with test_client.application.app_context():
        hubfile = Hubfile.query.first()
        if hubfile is None:
            feature_model = FeatureModel.query.first()

            hubfile = Hubfile(
                name="test_file.uvl",
                checksum="checksum123",
                size=2048,
                feature_model_id=feature_model.id
            )
            db.session.add(hubfile)
            db.session.commit()

        original_name = hubfile.name
        hubfile.name = "updated_file.uvl"
        db.session.commit()

        updated_hubfile = Hubfile.query.get(hubfile.id)
        assert updated_hubfile.name == "updated_file.uvl", \
            f"Expected updated name 'updated_file.uvl', got '{updated_hubfile.name}'."

        updated_hubfile.name = original_name
        db.session.commit()
