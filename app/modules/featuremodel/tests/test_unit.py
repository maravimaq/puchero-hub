import pytest
from app import db
from app.modules.dataset.models import DataSet, DSMetaData, Author, PublicationType
from app.modules.featuremodel.models import FeatureModel, FMMetaData, FMMetrics
from app.modules.featuremodel.services import FeatureModelService
from datetime import datetime
from app.modules.hubfile.models import Hubfile, HubfileDownloadRecord


feature_model_service = FeatureModelService()


@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        author_1 = Author(name="John Doe", affiliation="Test University", orcid="0000-0000-0000-0001")
        author_2 = Author(name="Jane Smith", affiliation="Another University", orcid="0000-0000-0000-0002")
        db.session.add(author_1)
        db.session.add(author_2)

        ds_metadata = DSMetaData(
            title="Sample Dataset",
            description="Description of the dataset",
            publication_type=PublicationType.REPORT,
            tags="sample, dataset",
            dataset_doi="10.1234/sample"
        )
        db.session.add(ds_metadata)
        db.session.commit()

        data_set = DataSet(
            user_id=1,
            ds_meta_data_id=ds_metadata.id,
            created_at=datetime.utcnow()
        )
        db.session.add(data_set)
        db.session.commit()

        metrics = FMMetrics(solver="SAT Solver 1", not_solver="Non-SAT Solver 2")
        db.session.add(metrics)

        fm_metadata_1 = FMMetaData(
            uvl_filename="model1.uvl",
            title="Feature Model 1",
            description="Description of Feature Model 1",
            publication_type=PublicationType.REPORT,
            publication_doi="10.1234/fm1",
            tags="test, feature model",
            uvl_version="1.0",
            fm_metrics=metrics
        )
        db.session.add(fm_metadata_1)
        db.session.commit()

        feature_model = FeatureModel(
            data_set_id=data_set.id,
            fm_meta_data=fm_metadata_1
        )
        db.session.add(feature_model)
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


def test_count_feature_models(test_client):
    """
    Test the count_feature_models method.
    """
    with test_client.application.app_context():
        count = feature_model_service.count_feature_models()
        assert count == 1, f"Expected 1 feature model, but got {count}."

def test_feature_model_metadata_relationship(test_client):
    """
    Test the relationship between FeatureModel and FMMetaData.
    """
    with test_client.application.app_context():
        feature_model = FeatureModel.query.first()
        assert feature_model is not None, "FeatureModel should exist in the database."
        assert feature_model.fm_meta_data is not None, "FeatureModel should have related metadata."
        assert feature_model.fm_meta_data.title == "Feature Model 1", \
            f"Expected title 'Feature Model 1', but got '{feature_model.fm_meta_data.title}'."


def test_fm_metrics_relationship(test_client):
    """
    Test the relationship between FMMetaData and FMMetrics.
    """
    with test_client.application.app_context():
        metadata = FMMetaData.query.first()
        assert metadata is not None, "FMMetaData should exist in the database."
        assert metadata.fm_metrics is not None, "FMMetaData should have related metrics."
        assert metadata.fm_metrics.solver == "SAT Solver 1", \
            f"Expected solver 'SAT Solver 1', but got '{metadata.fm_metrics.solver}'."


def test_retrieve_feature_model_by_dataset(test_client):
    """
    Test retrieving a FeatureModel by its associated DataSet ID.
    """
    with test_client.application.app_context():
        data_set = DataSet.query.first()
        assert data_set is not None, "DataSet should exist in the database."
        
        feature_model = FeatureModel.query.filter_by(data_set_id=data_set.id).first()
        assert feature_model is not None, "FeatureModel should exist for the given DataSet."
        assert feature_model.data_set_id == data_set.id, \
            f"Expected data_set_id {data_set.id}, but got {feature_model.data_set_id}."


def test_total_feature_model_downloads(test_client):
    """
    Test the total_feature_model_downloads method in the FeatureModelService.
    """
    with test_client.application.app_context():

        feature_model = FeatureModel.query.first()

        hubfile_1 = Hubfile(
            name="file1.uvl",
            checksum="abc123",
            size=1024,
            feature_model_id=feature_model.id
        )
        hubfile_2 = Hubfile(
            name="file2.xml",
            checksum="def456",
            size=2048,
            feature_model_id=feature_model.id
        )
        db.session.add(hubfile_1)
        db.session.add(hubfile_2)
        db.session.commit()

        download_1 = HubfileDownloadRecord(
            user_id=None,
            file_id=hubfile_1.id,
            download_cookie="cookie1"
        )
        download_2 = HubfileDownloadRecord(
            user_id=None,
            file_id=hubfile_2.id,
            download_cookie="cookie2"
        )
        download_3 = HubfileDownloadRecord(
            user_id=None,
            file_id=hubfile_1.id,
            download_cookie="cookie3"
        )
        db.session.add_all([download_1, download_2, download_3])
        db.session.commit()

        total_downloads = feature_model_service.total_feature_model_downloads()

        assert total_downloads == 3, f"Expected total downloads to be 3, but got {total_downloads}."


def test_add_new_fm_metadata(test_client):
    """
    Test adding a new FMMetaData entry to the database.
    """
    with test_client.application.app_context():
        new_metrics = FMMetrics(solver="New Solver", not_solver="New Non-Solver")
        db.session.add(new_metrics)
        db.session.commit()

        new_fm_metadata = FMMetaData(
            uvl_filename="new_model.uvl",
            title="New Feature Model",
            description="Description of the new feature model",
            publication_type=PublicationType.JOURNAL_ARTICLE,
            publication_doi="10.1234/new_fm",
            tags="new, test",
            uvl_version="1.1",
            fm_metrics=new_metrics
        )
        db.session.add(new_fm_metadata)
        db.session.commit()

        metadata = FMMetaData.query.filter_by(title="New Feature Model").first()
        assert metadata is not None, "New FMMetaData should be saved in the database."
        assert metadata.title == "New Feature Model", \
            f"Expected title 'New Feature Model', but got '{metadata.title}'."


def test_delete_feature_model_and_metadata(test_client):
    """
    Test deleting a FeatureModel and ensuring its related metadata and associated records are also deleted.
    """
    with test_client.application.app_context():
        feature_model = FeatureModel.query.first()
        assert feature_model is not None, "FeatureModel should exist in the database."

        hubfiles = Hubfile.query.filter_by(feature_model_id=feature_model.id).all()
        for hubfile in hubfiles:
            db.session.query(HubfileDownloadRecord).filter_by(file_id=hubfile.id).delete()
        
        db.session.query(Hubfile).filter_by(feature_model_id=feature_model.id).delete()

        metadata_id = feature_model.fm_meta_data_id
        db.session.delete(feature_model)
        db.session.commit()

        metadata = FMMetaData.query.get(metadata_id)
        assert metadata is None, "Related FMMetaData should be deleted when FeatureModel is deleted."


def test_update_fm_metadata(test_client):
    """
    Test updating an existing FMMetaData entry in the database.
    """
    with test_client.application.app_context():
        metadata = FMMetaData.query.first()
        assert metadata is not None, "FMMetaData should exist in the database."

        metadata.title = "Updated Feature Model"
        metadata.tags = "updated, feature model"
        db.session.commit()

        updated_metadata = FMMetaData.query.filter_by(id=metadata.id).first()
        assert updated_metadata is not None, "Updated FMMetaData should exist in the database."
        assert updated_metadata.title == "Updated Feature Model", \
            f"Expected title 'Updated Feature Model', but got '{updated_metadata.title}'."
        assert updated_metadata.tags == "updated, feature model", \
            f"Expected tags 'updated, feature model', but got '{updated_metadata.tags}'."


def test_retrieve_hubfiles_for_feature_model(test_client):
    """
    Test retrieving all Hubfile entries associated with a specific FeatureModel.
    """
    with test_client.application.app_context():
        feature_model = FeatureModel.query.first()
        if feature_model is None:
            ds_metadata = DSMetaData(
                title="Temporary Dataset",
                description="Temporary dataset description",
                publication_type=PublicationType.REPORT,
                tags="temporary, dataset",
                dataset_doi="10.1234/temp"
            )
            db.session.add(ds_metadata)
            db.session.commit()

            data_set = DataSet(
                user_id=1,
                ds_meta_data_id=ds_metadata.id,
                created_at=datetime.utcnow()
            )
            db.session.add(data_set)
            db.session.commit()

            fm_metadata = FMMetaData(
                uvl_filename="temp_model.uvl",
                title="Temporary Feature Model",
                description="Temporary feature model description",
                publication_type=PublicationType.REPORT,
                tags="temporary, feature model",
                uvl_version="1.0"
            )
            db.session.add(fm_metadata)
            db.session.commit()

            feature_model = FeatureModel(
                data_set_id=data_set.id,
                fm_meta_data=fm_metadata
            )
            db.session.add(feature_model)
            db.session.commit()

        hubfile_1 = Hubfile(
            name="temp_file1.uvl",
            checksum="checksum1",
            size=512,
            feature_model_id=feature_model.id
        )
        hubfile_2 = Hubfile(
            name="temp_file2.xml",
            checksum="checksum2",
            size=2048,
            feature_model_id=feature_model.id
        )
        db.session.add_all([hubfile_1, hubfile_2])
        db.session.commit()

        hubfiles = Hubfile.query.filter_by(feature_model_id=feature_model.id).all()
        assert len(hubfiles) == 2, f"Expected 2 Hubfiles for the FeatureModel, but got {len(hubfiles)}."
        assert hubfiles[0].name == "temp_file1.uvl", f"Expected first Hubfile name 'temp_file1.uvl', but got '{hubfiles[0].name}'."
        assert hubfiles[1].name == "temp_file2.xml", f"Expected second Hubfile name 'temp_file2.xml', but got '{hubfiles[1].name}'."
