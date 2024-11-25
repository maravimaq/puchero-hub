import pytest
import os
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


def test_hubfile_get_formatted_size_edge_cases(test_client):
    """
    Test the `get_formatted_size()` method for various edge cases.
    """
    with test_client.application.app_context():
        hubfile = Hubfile.query.first()
        assert hubfile is not None, "Hubfile should exist in the database."

        hubfile.size = 2048
        db.session.commit()
        assert hubfile.get_formatted_size().startswith("2") and hubfile.get_formatted_size().endswith("KB")

        hubfile.size = 2 * 1024 * 1024 - 1
        db.session.commit()
        assert hubfile.get_formatted_size().startswith("2") and hubfile.get_formatted_size().endswith("MB")


def test_hubfile_to_dict_edge_cases(test_client):
    """
    Test the `to_dict()` method for Hubfile with edge cases.
    """
    with test_client.application.app_context():
        hubfile = Hubfile.query.first()
        assert hubfile is not None, "Hubfile should exist in the database."

        hubfile.name = "edge_case_file"
        hubfile.size = 0
        db.session.commit()

        with test_client.application.test_request_context('/'):
            hubfile_dict = hubfile.to_dict()
            assert hubfile_dict["name"] == hubfile.name, f"Expected name '{hubfile.name}', got {hubfile_dict['name']}."
            assert hubfile_dict["size_in_bytes"] == 0, f"Expected size_in_bytes 0, got {hubfile_dict['size_in_bytes']}."
            assert "url" in hubfile_dict, "Expected 'url' key in the dictionary."

        hubfile.name = "test_file.uvl"
        hubfile.size = 2048
        db.session.commit()


def test_get_dataset_by_hubfile(test_client):
    """
    Test `HubfileRepository.get_dataset_by_hubfile()` method.
    """
    from app.modules.hubfile.repositories import HubfileRepository

    with test_client.application.app_context():
        repo = HubfileRepository()
        hubfile = Hubfile.query.first()
        assert hubfile is not None, "Hubfile should exist in the database."

        dataset = repo.get_dataset_by_hubfile(hubfile)

        assert dataset is not None, "Dataset should exist for a valid Hubfile."
        assert dataset.ds_meta_data.title == "Sample Dataset", \
            f"Expected dataset title 'Sample Dataset', got '{dataset.ds_meta_data.title}'."


def test_hubfile_with_missing_feature_model(test_client):
    """
    Test Hubfile's behavior when the associated FeatureModel is missing.
    """
    with test_client.application.app_context():
        hubfile = Hubfile.query.first()
        assert hubfile is not None, "Hubfile should exist in the database."

        feature_model_id = hubfile.feature_model_id

        feature_model = FeatureModel.query.get(feature_model_id)
        assert feature_model is not None, "FeatureModel associated with Hubfile should exist."
        db.session.delete(feature_model)
        db.session.commit()

        hubfile = Hubfile.query.filter_by(id=hubfile.id).first()
        if hubfile is None:
            assert True, "Hubfile was deleted due to cascading delete from the FeatureModel."
        else:
            assert hubfile.feature_model_id == feature_model_id, \
                "Hubfile should still reference the deleted FeatureModel."



def test_hubfile_invalid_data(test_client):
    """
    Test that invalid data raises exceptions or errors appropriately.
    """
    with test_client.application.app_context():
        with pytest.raises(Exception):
            invalid_hubfile = Hubfile(name=None, checksum=None, size=-1)
            db.session.add(invalid_hubfile)
            db.session.commit()


def test_download_file_existing(test_client):
    """
    Test `/file/download/<id>` route for an existing file.
    """
    with test_client.application.app_context():
        feature_model = FeatureModel.query.first()
        if not feature_model:
            fm_metrics = FMMetrics(solver="SAT Solver", not_solver="Non-SAT Solver")
            db.session.add(fm_metrics)
            db.session.commit()

            fm_metadata = FMMetaData(
                uvl_filename="test_model.uvl",
                title="Test Feature Model",
                description="Feature Model for testing",
                publication_type="REPORT",
                tags="test,featuremodel",
                uvl_version="1.0",
                fm_metrics_id=fm_metrics.id
            )
            db.session.add(fm_metadata)
            db.session.commit()

            feature_model = FeatureModel(
                data_set_id=1,
                fm_meta_data_id=fm_metadata.id
            )
            db.session.add(feature_model)
            db.session.commit()

        hubfile = Hubfile.query.first()
        if not hubfile:
            hubfile = Hubfile(
                name="test_file.uvl",
                checksum="checksum123",
                size=2048,
                feature_model_id=feature_model.id
            )
            db.session.add(hubfile)
            db.session.commit()

        file_directory = os.path.join(
            os.path.dirname(test_client.application.root_path),
            f"uploads/user_{feature_model.data_set_id}/dataset_{feature_model.data_set_id}/"
        )
        os.makedirs(file_directory, exist_ok=True)
        file_path = os.path.join(file_directory, hubfile.name)
        with open(file_path, "w") as f:
            f.write("Test content")

    response = test_client.get(f"/file/download/{hubfile.id}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}."
    assert "Content-Disposition" in response.headers, "Response should contain Content-Disposition header."
    assert f"filename={hubfile.name}" in response.headers["Content-Disposition"], \
        f"Expected filename in Content-Disposition, got {response.headers['Content-Disposition']}."


def test_download_file_nonexistent(test_client):
    """
    Test `/file/download/<id>` route for a non-existent file.
    """
    invalid_file_id = 9999
    response = test_client.get(f"/file/download/{invalid_file_id}")

    assert response.status_code == 404, f"Expected status code 404, got {response.status_code}."

    assert "text/html" in response.content_type, f"Expected content type 'text/html', got {response.content_type}."

    assert b"Page Not Found" in response.data, "Expected 'Page Not Found' in the HTML response."


def test_view_file_existing(test_client):
    """
    Test `/file/view/<id>` route for an existing file.
    """
    with test_client.application.app_context():
        feature_model = FeatureModel.query.first()
        if not feature_model:
            fm_metrics = FMMetrics(solver="SAT Solver", not_solver="Non-SAT Solver")
            db.session.add(fm_metrics)
            db.session.commit()

            fm_metadata = FMMetaData(
                uvl_filename="test_model.uvl",
                title="Test Feature Model",
                description="Feature Model for testing",
                publication_type="REPORT",
                tags="test,featuremodel",
                uvl_version="1.0",
                fm_metrics_id=fm_metrics.id
            )
            db.session.add(fm_metadata)
            db.session.commit()

            feature_model = FeatureModel(
                data_set_id=1,
                fm_meta_data_id=fm_metadata.id
            )
            db.session.add(feature_model)
            db.session.commit()

        hubfile = Hubfile.query.first()
        if not hubfile:
            hubfile = Hubfile(
                name="test_file.uvl",
                checksum="checksum123",
                size=2048,
                feature_model_id=feature_model.id
            )
            db.session.add(hubfile)
            db.session.commit()

        file_directory = os.path.join(
            os.path.dirname(test_client.application.root_path),
            f"uploads/user_{feature_model.data_set_id}/dataset_{feature_model.data_set_id}/"
        )
        os.makedirs(file_directory, exist_ok=True)
        file_path = os.path.join(file_directory, hubfile.name)
        with open(file_path, "w") as f:
            f.write("Test content for viewing")

    response = test_client.get(f"/file/view/{hubfile.id}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}."
    assert response.is_json, "Expected JSON response."
    data = response.get_json()
    assert data["success"], "Expected success to be True in the JSON response."
    assert "content" in data, "Expected 'content' key in the JSON response."
    assert data["content"] == "Test content for viewing", "Unexpected file content in response."


def test_view_file_nonexistent(test_client):
    """
    Test `/file/view/<id>` route for a nonexistent file.
    """
    invalid_file_id = 9999
    response = test_client.get(f"/file/view/{invalid_file_id}")

    assert response.status_code == 404, f"Expected status code 404, got {response.status_code}."
    
    assert "text/html" in response.content_type, f"Expected content type 'text/html', got {response.content_type}."
    
    assert b"Page Not Found" in response.data, "Expected 'Page Not Found' in the HTML response."


def test_get_owner_user_by_hubfile(test_client):
    """
    Test `get_owner_user_by_hubfile` method.
    """
    from app.modules.hubfile.services import HubfileService

    with test_client.application.app_context():
        service = HubfileService()
        hubfile = Hubfile.query.first()
        assert hubfile is not None, "Hubfile should exist in the database."

        owner_user = service.get_owner_user_by_hubfile(hubfile)
        assert owner_user is not None, "Owner user should be returned."
        assert owner_user.email == "test@example.com", \
            f"Expected email 'test@example.com', got '{owner_user.email}'."


def test_get_path_by_hubfile(test_client):
    """
    Test `get_path_by_hubfile` method.
    """
    from app.modules.hubfile.services import HubfileService

    with test_client.application.app_context():
        service = HubfileService()
        hubfile = Hubfile.query.first()
        assert hubfile is not None, "Hubfile should exist in the database."

        os.environ["WORKING_DIR"] = "/test/working/dir"

        path = service.get_path_by_hubfile(hubfile)
        expected_path = f"/test/working/dir/uploads/user_1/dataset_1/{hubfile.name}"
        assert path == expected_path, f"Expected path '{expected_path}', got '{path}'."


def test_total_hubfile_views(test_client):
    """
    Test `total_hubfile_views` method.
    """
    from app.modules.hubfile.services import HubfileService

    with test_client.application.app_context():
        service = HubfileService()

        total_views = service.total_hubfile_views()
        assert total_views == 2, f"Expected total views 2, got {total_views}."


def test_total_hubfile_downloads(test_client):
    """
    Test `total_hubfile_downloads` method.
    """
    from app.modules.hubfile.services import HubfileService

    with test_client.application.app_context():
        service = HubfileService()

        total_downloads = service.total_hubfile_downloads()
        assert total_downloads == 2, f"Expected total downloads 2, got {total_downloads}."


def test_create_download_record(test_client):
    """
    Test creating a new download record using `HubfileDownloadRecordService`.
    """
    from app.modules.hubfile.services import HubfileDownloadRecordService

    with test_client.application.app_context():
        service = HubfileDownloadRecordService()
        hubfile = Hubfile.query.first()
        assert hubfile is not None, "Hubfile should exist in the database."

        new_record = service.create(
            user_id=1,
            file_id=hubfile.id,
            download_date=datetime.utcnow(),
            download_cookie="new_download_cookie"
        )
        assert new_record is not None, "Download record should be created."
        assert new_record.download_cookie == "new_download_cookie", \
            f"Expected download cookie 'new_download_cookie', got '{new_record.download_cookie}'."


def test_hubfile_to_dict_edge_cases(test_client):
    """
    Test the `to_dict()` method of Hubfile for edge cases.
    """
    with test_client.application.app_context():
        hubfile = Hubfile.query.first()
        assert hubfile is not None, "Hubfile should exist in the database."

        hubfile.name = ""
        hubfile.checksum = ""
        db.session.commit()

        with test_client.application.test_request_context('/'):
            hubfile_dict = hubfile.to_dict()
            assert hubfile_dict["name"] == "", "Expected empty name."
            assert hubfile_dict["checksum"] == "", "Expected empty checksum."
            assert hubfile_dict["size_in_bytes"] == hubfile.size, "Expected size to remain the same."
            assert "url" in hubfile_dict, "Expected 'url' key even for edge cases."

        hubfile.name = "test_file.uvl"
        hubfile.checksum = "checksum123"
        db.session.commit()


def test_hubfile_get_formatted_size_extended(test_client):
    """
    Extended test for `get_formatted_size` method of Hubfile, without mocking.
    """
    with test_client.application.app_context():
        hubfile = Hubfile.query.first()
        assert hubfile is not None, "Hubfile should exist in the database."

        hubfile.size = 0
        db.session.commit()
        formatted_size = hubfile.get_formatted_size()
        assert formatted_size == "0 bytes", f"Expected '0 bytes', got '{formatted_size}'."

        hubfile.size = -1024
        db.session.commit()
        formatted_size = hubfile.get_formatted_size()
        assert formatted_size == "-1024 bytes", f"Expected '-1024 bytes', got '{formatted_size}' for negative size."

        hubfile.size = 2 * 1024 * 1024 * 1024 - 1
        db.session.commit()
        formatted_size = hubfile.get_formatted_size()
        assert "GB" in formatted_size, f"Expected size in GB, got '{formatted_size}'."

        hubfile.size = 1024 * 1024 + 1
        db.session.commit()
        formatted_size = hubfile.get_formatted_size()
        assert "MB" in formatted_size, f"Expected size close to 1 MB, got '{formatted_size}'."

        # Revert changes
        hubfile.size = 2048
        db.session.commit()
