import pytest
from app import db, create_app
from app.modules.dataset.models import DataSet, DSMetaData, PublicationType, Author
from app.modules.auth.models import User


@pytest.fixture
def app():
    app = create_app('testing')  # Ensure 'testing' config is set up
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def populate_data(app):
    with app.app_context():
        # Create a test user
        user = User(email="testuser@example.com", password="password")
        db.session.add(user)
        db.session.commit()

        # Create authors
        author1 = Author(name="Author One")
        author2 = Author(name="Author Two")
        db.session.add_all([author1, author2])
        db.session.commit()

        # Create metadata
        meta1 = DSMetaData(
            title="Dataset 1",
            description="A test dataset",
            publication_type=PublicationType.JOURNAL_ARTICLE.name,
            authors=[author1],
            publication_doi="10.1234/example-1",
            tags="test"
        )
        meta2 = DSMetaData(
            title="Dataset 2",
            description="Another test dataset",
            publication_type=PublicationType.BOOK.name,
            authors=[author2],
            publication_doi="10.1234/example-2",
            tags="test"
        )
        db.session.add_all([meta1, meta2])
        db.session.commit()

        # Create datasets and associate with the user
        dataset1 = DataSet(user_id=user.id, ds_meta_data_id=meta1.id)
        dataset2 = DataSet(user_id=user.id, ds_meta_data_id=meta2.id)
        db.session.add_all([dataset1, dataset2])
        db.session.commit()


def test_explore_post_filter_by_title(client, populate_data):
    criteria = {
        "title": "Dataset 1",
        "publication_type": "journal_article"
    }
    response = client.post('/explore', json=criteria)
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 1
    assert json_data[0]['title'] == "Dataset 1"


def test_explore_post_no_results(client, populate_data):
    criteria = {
        "title": "Nonexistent Dataset"
    }
    response = client.post('/explore', json=criteria)
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 0


def test_explore_post_filter_by_author(client, populate_data):
    criteria = {
        "author": "Author One"
    }
    response = client.post('/explore', json=criteria)
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 1
    assert json_data[0]['title'] == "Dataset 1"


def test_explore_post_filter_by_multiple_criteria(client, populate_data):
    criteria = {
        "author": "Author One",
        "publication_type": "journal_article"
    }
    response = client.post('/explore', json=criteria)
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 1
    assert json_data[0]['title'] == "Dataset 1"


def test_explore_post_filter_by_partial_title(client, populate_data):
    criteria = {
        "title": "Dataset"
    }
    response = client.post('/explore', json=criteria)
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 2
    assert any(dataset['title'] == "Dataset 1" for dataset in json_data)
    assert any(dataset['title'] == "Dataset 2" for dataset in json_data)


def test_explore_post_empty_filter(client, populate_data):
    # An empty filter should return all datasets
    response = client.post('/explore', json={})
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 2
    assert any(dataset['title'] == "Dataset 1" for dataset in json_data)
    assert any(dataset['title'] == "Dataset 2" for dataset in json_data)


def test_explore_post_filter_by_nonexistent_author(client, populate_data):
    criteria = {
        "author": "Nonexistent Author"
    }
    response = client.post('/explore', json=criteria)
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 0  # No datasets should match


def test_explore_post_filter_by_tags(client, populate_data):
    criteria = {
        "tags": "test"
    }
    response = client.post('/explore', json=criteria)
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 2  # Assuming both datasets have the "test" tag
    assert any(dataset['title'] == "Dataset 1" for dataset in json_data)
    assert any(dataset['title'] == "Dataset 2" for dataset in json_data)


def test_explore_post_filter_by_date_range(client, populate_data):
    criteria = {
        "date_from": "2024-01-01",
        "date_to": "2024-12-31"
    }
    response = client.post('/explore', json=criteria)
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 2  # Both datasets fall within this range
    assert any(dataset['title'] == "Dataset 1" for dataset in json_data)
    assert any(dataset['title'] == "Dataset 2" for dataset in json_data)


def test_explore_post_filter_by_multiple_authors(client, populate_data):
    criteria = {
        "authors": ["Author One", "Author Two"]
    }
    response = client.post('/explore', json=criteria)
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 2
    assert any(dataset['title'] == "Dataset 1" for dataset in json_data)
    assert any(dataset['title'] == "Dataset 2" for dataset in json_data)


def test_explore_get_all_datasets(client, populate_data):
    """
    Test the GET method of the /explore endpoint to retrieve and render all datasets.
    """
    response = client.get('/explore')
    assert response.status_code == 200

    # Verify the page title
    assert b"<h1 class=\"h2 mb-3\"><b>Explore</b></h1>" in response.data

    # Verify that dataset titles are rendered
    assert b"Dataset 1" in response.data
    assert b"Dataset 2" in response.data

    # Ensure "not found" div is not visible
    assert b"id=\"results_not_found\" style=\"display: none;\"" in response.data


def test_explore_post_filter_by_description(client, populate_data):
    criteria = {
        "description": "A test dataset"
    }
    response = client.post('/explore', json=criteria)
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 1
    assert json_data[0]['title'] == "Dataset 1"
