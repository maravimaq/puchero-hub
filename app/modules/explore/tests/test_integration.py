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
        )
        meta2 = DSMetaData(
            title="Dataset 2",
            description="Another test dataset",
            publication_type=PublicationType.BOOK.name,
            authors=[author2],
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
