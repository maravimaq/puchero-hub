import pytest
from app.modules.explore.services import ExploreService
from app.modules.dataset.models import DataSet, DSMetaData, Author, PublicationType
from app import db

explore_service = ExploreService()


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test client fixture to add test data for the Explore module.
    """
    with test_client.application.app_context():
        from app.modules.auth.models import User
        user_1 = User(email="user1@example.com", password="password1")
        user_2 = User(email="user2@example.com", password="password2")
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()

        author_1 = Author(name="John Doe", affiliation="Test University", orcid="0000-0000-0000-0001")
        author_2 = Author(name="Jane Smith", affiliation="Another University", orcid="0000-0000-0000-0002")
        db.session.add(author_1)
        db.session.add(author_2)

        metadata_1 = DSMetaData(
            title="Climate Change Data",
            description="A dataset about climate change.",
            publication_type=PublicationType.REPORT,
            tags="climate, environment",
            dataset_doi="10.1234/example-1",
        )
        metadata_2 = DSMetaData(
            title="Genomics Research",
            description="Genomic analysis dataset.",
            publication_type=PublicationType.JOURNAL_ARTICLE,
            tags="genomics, dna",
            dataset_doi="10.1234/example-2",
        )
        db.session.add(metadata_1)
        db.session.add(metadata_2)
        db.session.commit()

        metadata_1.authors.append(author_1)
        metadata_2.authors.append(author_2)

        from datetime import datetime, timedelta
        dataset_1 = DataSet(
            user_id=user_1.id,
            ds_meta_data_id=metadata_1.id,
            created_at=datetime.utcnow() - timedelta(days=1)
        )
        dataset_2 = DataSet(
            user_id=user_2.id,
            ds_meta_data_id=metadata_2.id,
            created_at=datetime.utcnow()
        )
        db.session.add(dataset_1)
        db.session.add(dataset_2)
        db.session.commit()

    yield test_client



def test_filter_by_query(test_client):
    """
    Test filtering datasets by query string.
    """
    with test_client.application.app_context():
        results = DataSet.query.join(DataSet.ds_meta_data).filter(
            DSMetaData.title.ilike('%climate%')
        ).all()

        assert len(results) == 1, "Expected only one dataset matching 'climate'."
        assert results[0].ds_meta_data.title == "Climate Change Data", \
            "The dataset title did not match the expected result."


def test_filter_by_tags(test_client):
    """
    Test filtering datasets by tags.
    """
    with test_client.application.app_context():
        results = DataSet.query.join(DataSet.ds_meta_data).filter(
            DSMetaData.tags.ilike('%climate%')
        ).all()

        assert len(results) == 1, "Expected only one dataset matching the tag 'climate'."
        assert results[0].ds_meta_data.title == "Climate Change Data", \
            "The dataset title did not match the expected result for the tag 'climate'."


def test_sort_by_date(test_client):
    """
    Test sorting datasets by creation date.
    """
    with test_client.application.app_context():
        results = DataSet.query.order_by(DataSet.created_at.desc()).all()

        assert len(results) == 2, "Expected two datasets in the database."
        assert results[0].created_at > results[1].created_at, \
            "Datasets are not correctly ordered by creation date."
        assert results[0].ds_meta_data.title == "Genomics Research", \
            f"The newest dataset should be 'Genomics Research', but got '{results[0].ds_meta_data.title}'."
        assert results[1].ds_meta_data.title == "Climate Change Data", \
            f"The oldest dataset should be 'Climate Change Data', but got '{results[1].ds_meta_data.title}'."


def test_filter_by_multiple_criteria(test_client):
    """
    Test filtering datasets by multiple criteria (query and tags).
    """
    with test_client.application.app_context():
        results = DataSet.query.join(DataSet.ds_meta_data).filter(
            DSMetaData.title.ilike('%climate%'),
            DSMetaData.tags.ilike('%environment%')
        ).all()

        assert len(results) == 1, "Expected only one dataset matching 'climate' and 'environment'."
        assert results[0].ds_meta_data.title == "Climate Change Data", \
            "The dataset title did not match the expected result."


def test_sort_and_filter_combined(test_client):
    """
    Test sorting datasets by creation date while filtering by tags.
    """
    with test_client.application.app_context():
        results = DataSet.query.join(DataSet.ds_meta_data).filter(
            DSMetaData.tags.ilike('%dna%')
        ).order_by(DataSet.created_at.desc()).all()

        assert len(results) == 1, "Expected only one dataset matching the tag 'dna'."
        assert results[0].ds_meta_data.title == "Genomics Research", \
            "The dataset title did not match the expected result for the tag 'dna'."


def test_filter_by_publication_type(test_client):
    """
    Test filtering datasets by publication type.
    """
    with test_client.application.app_context():
        results = DataSet.query.join(DataSet.ds_meta_data).filter(
            DSMetaData.publication_type == PublicationType.REPORT.name
        ).all()

        assert len(results) == 1, "Expected only one dataset with publication type 'REPORT'."
        assert results[0].ds_meta_data.title == "Climate Change Data", \
            "The dataset title did not match the expected result for publication type 'REPORT'."

def test_filter_by_author_name(test_client):
    """
    Test filtering datasets by author name.
    """
    with test_client.application.app_context():
        results = DataSet.query.join(DataSet.ds_meta_data).join(DSMetaData.authors).filter(
            Author.name.ilike('%John Doe%')
        ).all()

        assert len(results) == 1, "Expected only one dataset authored by 'John Doe'."
        assert results[0].ds_meta_data.title == "Climate Change Data", \
            "The dataset title did not match the expected result for author 'John Doe'."


def test_pagination(test_client):
    """
    Test pagination of datasets.
    """
    with test_client.application.app_context():
        page = 1
        per_page = 1
        paginated_results = DataSet.query.paginate(page=page, per_page=per_page, error_out=False)

        assert paginated_results.total == 2, "Expected two total datasets in the database."
        assert len(paginated_results.items) == 1, "Expected only one dataset per page."
        assert paginated_results.items[0].ds_meta_data.title in ["Climate Change Data", "Genomics Research"], \
            "The paginated result did not match any expected dataset titles."
