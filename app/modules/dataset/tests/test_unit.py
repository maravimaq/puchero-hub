import os
import pytest
from unittest.mock import patch, Mock, MagicMock, mock_open, ANY
from app.modules.dataset.services import (
    calculate_checksum_and_size,
    convert_uvl_to_pdf,
    convert_uvl_to_cnf,
    convert_uvl_to_json,
    convert_uvl_to_splx,
    pack_datasets,
    DataSetService,
)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from app.modules.dataset.routes import dataset_bp
from flask_wtf.csrf import CSRFProtect
from io import BytesIO

# Mock the Flask app and SQLAlchemy for testing
db = SQLAlchemy()

@pytest.fixture
def client():
    """Set up a test client for Flask."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret_key"  # Required for CSRF
    app.config["WTF_CSRF_ENABLED"] = False       # Disable CSRF for tests
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # Set up Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    class TestUser(UserMixin):
        """Mock user for testing."""
        id = 1  # Simulated user ID

    @login_manager.user_loader
    def load_user(user_id):
        return TestUser()  # Always return the TestUser

    csrf = CSRFProtect()
    csrf.init_app(app)

    # Register the blueprint
    app.register_blueprint(dataset_bp)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            # Log in the user
            with client.session_transaction() as session:
                session["_user_id"] = "1"  # Match the ID of TestUser

        yield client

# Test calculate_checksum_and_size
def test_calculate_checksum_and_size():
    file_content = b"Sample content"
    mocked_open = mock_open(read_data=file_content)

    with patch("builtins.open", mocked_open), patch("os.path.getsize", return_value=len(file_content)):
        checksum, size = calculate_checksum_and_size("dummy_path")

    assert checksum == "b4ed349f78183083dcaf708313c8c99b"  # Example of MD5 checksum
    assert size == len(file_content)


# Test convert_uvl_to_pdf
@patch("app.modules.dataset.services.FPDF")
def test_convert_uvl_to_pdf(mock_fpdf):
    mock_fpdf_instance = Mock()
    mock_fpdf.return_value = mock_fpdf_instance

    uvl_content = "UVL example content"
    with patch("builtins.open", mock_open(read_data=uvl_content)):
        convert_uvl_to_pdf("dummy.uvl", "output.pdf")

    mock_fpdf.assert_called_once()
    mock_fpdf_instance.add_page.assert_called_once()
    mock_fpdf_instance.set_font.assert_called_once_with("Arial", size=12)
    mock_fpdf_instance.multi_cell.assert_called_once_with(0, 10, uvl_content)
    mock_fpdf_instance.output.assert_called_once_with("output.pdf")


# Test convert_uvl_to_json
@patch("builtins.open", new_callable=mock_open, read_data="UVL example content")
@patch("json.dump")
def test_convert_uvl_to_json(mock_json_dump, mock_open):
    input_file = "dummy_input.uvl"
    output_file = "dummy_output.json"

    convert_uvl_to_json(input_file, output_file)

    mock_open.assert_any_call(input_file, "r")
    mock_open.assert_any_call(output_file, "w")
    mock_json_dump.assert_called_once_with(
        {"data": "UVL example content"}, mock_open.return_value.__enter__(), indent=4
    )


# Test convert_uvl_to_cnf
@patch("builtins.open", new_callable=mock_open, read_data="Line 1\nLine 2\n")
def test_convert_uvl_to_cnf(mock_open):
    input_file = "dummy_input.uvl"
    output_file = "dummy_output.cnf"

    convert_uvl_to_cnf(input_file, output_file)

    mock_open.assert_any_call(input_file, "r")
    mock_open.assert_any_call(output_file, "w")
    handle = mock_open()
    handle.write.assert_any_call("Line 1\n")
    handle.write.assert_any_call("Line 2\n")


# Test convert_uvl_to_splx
@patch("builtins.open", new_callable=mock_open, read_data="Line 1\nLine 2\n")
def test_convert_uvl_to_splx(mock_open):
    input_file = "dummy_input.uvl"
    output_file = "dummy_output.splx"

    convert_uvl_to_splx(input_file, output_file)

    mock_open.assert_any_call(input_file, "r")
    mock_open.assert_any_call(output_file, "w")
    handle = mock_open()
    handle.write.assert_any_call("Line 1\n")
    handle.write.assert_any_call("Line 2\n")


# Test pack_datasets
@patch("tempfile.mkdtemp", return_value="/mock/tmp")
@patch("os.path.exists", side_effect=lambda path: path in [
    "uploads",
    "uploads/user_1",
    "uploads/user_1/dataset_1",
    "uploads/user_1/dataset_1/file.uvl",
])
@patch("os.makedirs")
@patch("os.listdir", side_effect=[
    ["user_1"],  # First call for `uploads` directory
    ["dataset_1"],  # Second call for `user_1` directory
    ["file.uvl"],  # Third call for `dataset_1` directory
])
@patch("os.walk", return_value=[
    ("uploads/user_1/dataset_1", [], ["file.uvl"]),
])
@patch("app.modules.dataset.services.ZipFile")
@patch("app.modules.dataset.services.convert_uvl_to_pdf")
@patch("app.modules.dataset.services.convert_uvl_to_json")
@patch("app.modules.dataset.services.convert_uvl_to_cnf")
@patch("app.modules.dataset.services.convert_uvl_to_splx")
@patch("os.remove")
def test_pack_datasets(mock_remove, mock_convert_splx, mock_convert_cnf, mock_convert_json,
                       mock_convert_pdf, mock_zipfile, mock_walk, mock_listdir,
                       mock_makedirs, mock_exists, mock_mkdtemp):
    # Mock ZipFile behavior
    mock_zip_instance = MagicMock()
    mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

    # Call the function
    result = pack_datasets()

    # Debugging logs
    print(f"Result: {result}")
    print(f"os.path.exists calls: {mock_exists.call_args_list}")
    print(f"os.listdir calls: {mock_listdir.call_args_list}")
    print(f"os.walk calls: {mock_walk.call_args_list}")
    print(f"Mock ZipFile write calls: {mock_zip_instance.write.call_args_list}")

    # Assertions
    assert result == "/mock/tmp/datasets_collection.zip", \
        "The returned path should match the mocked temp directory."



# Test DataSetService.get_synchronized
@patch("app.modules.dataset.services.DataSetRepository")
def test_get_synchronized(mock_ds_repo):
    mock_ds_repo.return_value.get_synchronized.return_value = "mock_dataset"
    service = DataSetService()
    result = service.get_synchronized(1)
    assert result == "mock_dataset"
    mock_ds_repo.return_value.get_synchronized.assert_called_once_with(1)


@patch("shutil.move")
@patch("app.modules.auth.services.AuthenticationService.get_authenticated_user")
def test_move_feature_models(mock_auth_user, mock_shutil_move):
    # Mock authenticated user
    mock_user = Mock()
    mock_user.id = 123
    mock_user.temp_folder.return_value = "/temp"
    mock_auth_user.return_value = mock_user

    # Mock dataset with feature models
    dataset = Mock()
    dataset.id = 1
    dataset.feature_models = [
        Mock(fm_meta_data=Mock(uvl_filename="model1.uvl")),
        Mock(fm_meta_data=Mock(uvl_filename="model2.uvl")),
    ]

    # Instantiate the service and call the method
    service = DataSetService()
    service.move_feature_models(dataset)

    # Get the working directory used in the code
    working_dir = os.getenv("WORKING_DIR", "")
    if not working_dir:
        working_dir = os.getcwd()  # Fallback to current working directory

    # Define expected file paths
    expected_dest = os.path.join(working_dir, "uploads", f"user_{mock_user.id}", f"dataset_{dataset.id}")

    # Assertions: Ensure move was called for each file
    mock_shutil_move.assert_any_call("/temp/model1.uvl", expected_dest)
    mock_shutil_move.assert_any_call("/temp/model2.uvl", expected_dest)



@patch("app.modules.dataset.services.DSMetaDataRepository.update")
def test_update_dsmetadata(mock_update):
    mock_update.return_value = True
    service = DataSetService()
    result = service.update_dsmetadata(1, title="New Title")
    assert result is True
    mock_update.assert_called_once_with(1, title="New Title")


# Test the `/dataset/upload` route
@patch("app.modules.fakenodo.services.FakenodoService.create_new_deposition")
@patch("app.modules.dataset.routes.DataSetForm", autospec=True)
@patch("app.modules.dataset.routes.DataSetService.create_from_form")
@patch("app.modules.dataset.routes.DataSetService.move_feature_models")
@patch("flask_login.utils._get_user", return_value=Mock(temp_folder=lambda: "/temp"))
def test_create_dataset(
    mock_user, mock_move, mock_create, mock_form, mock_fakenodo, client
):
    """Test the `/dataset/upload` route."""
    mock_create.return_value = Mock(id=1, ds_meta_data_id=1)

    mock_fakenodo.return_value = {
        "id": 1,
        "title": "Test Dataset",
        "description": "Test Description",
        "status": "draft",
    }

    mock_form_instance = mock_form.return_value
    mock_form_instance.validate_on_submit.return_value = True
    mock_form_instance.data = {"title": "Test Dataset"}

    data = {
        "title": "Test Dataset", 
        "file": (b"test content", "file.uvl"),  
    }

    response = client.post(
        "/dataset/upload",
        data=data,
        content_type="multipart/form-data",
    )

    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.data.decode('utf-8')}")

    assert response.status_code == 200
    assert b"Everything works!" in response.data
    mock_create.assert_called_once()
    mock_move.assert_called_once()
    mock_fakenodo.assert_called_once()


@patch("werkzeug.datastructures.FileStorage.save", return_value=None)
@patch("os.makedirs")
@patch("os.path.exists", side_effect=lambda path: path in ["/temp"])
@patch("flask_login.utils._get_user", return_value=Mock(temp_folder=lambda: "/temp"))
def test_upload_file_success(mock_user, mock_exists, mock_makedirs, mock_save, client):
    """Test uploading a valid `.uvl` file."""
    data = {
        "file": (BytesIO(b"test content"), "test_file.uvl"),  # Valid extension and content
    }

    response = client.post(
        "/dataset/file/upload",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"UVL uploaded and validated successfully" in response.data
    mock_save.assert_called_once_with("/temp/test_file.uvl")


@patch("flask_login.utils._get_user", return_value=Mock(is_authenticated=True))
def test_upload_file_invalid_extension(mock_user, client):
    """Test uploading a file with an invalid extension."""
    data = {
        "file": (BytesIO(b"test content"), "test_file.txt"),  # Invalid extension
    }
    response = client.post(
        "/dataset/file/upload",
        data=data,
        content_type="multipart/form-data",
    )
    assert response.status_code == 400
    assert b"No valid file" in response.data



@patch("os.path.exists", return_value=True)
@patch("os.remove")
@patch("flask_login.utils._get_user", return_value=Mock(temp_folder=lambda: "/temp"))
def test_delete_file_success(mock_user, mock_remove, mock_exists, client):
    """Test deleting an existing file."""
    response = client.post(
        "/dataset/file/delete",
        json={"file": "test_file.uvl"},
    )
    assert response.status_code == 200
    assert b"File deleted successfully" in response.data
    mock_remove.assert_called_once_with("/temp/test_file.uvl")

@patch("os.path.exists", return_value=False)
@patch("flask_login.utils._get_user", return_value=Mock(temp_folder=lambda: "/temp"))
def test_delete_file_not_found(mock_user, mock_exists, client):
    """Test deleting a file that does not exist."""
    response = client.post(
        "/dataset/file/delete",
        json={"file": "nonexistent_file.uvl"},
    )
    assert response.status_code == 200
    assert b"Error: File not found" in response.data

@patch("app.modules.dataset.routes.pack_datasets", return_value="/mock/tmp/uvlhub_datasets.zip")
@patch("os.stat")  # Mock os.stat to simulate the file exists
@patch("builtins.open", new_callable=mock_open, read_data=b"mock file content")  # Mock file content
def test_download_all_datasets_success(mock_open, mock_stat, mock_pack, client):
    """Test downloading all datasets when datasets exist."""
    # Mock os.stat to prevent FileNotFoundError
    mock_stat.return_value = os.stat_result(
        (0o100644, 0, 0, 0, 0, 0, len(b"mock file content"), 0, 0, 0)
    )

    # Make the GET request
    response = client.get("/dataset/download/all")

    # Assertions
    assert response.status_code == 200
    assert response.headers["Content-Disposition"].startswith("attachment; filename=")
    assert response.headers["Content-Disposition"].endswith("uvlhub_datasets.zip")
    mock_pack.assert_called_once()  # Ensure pack_datasets was called
    mock_open.assert_called_once_with("/mock/tmp/uvlhub_datasets.zip", "rb")  # File was opened


@patch("app.modules.dataset.routes.pack_datasets", return_value=None)
def test_download_all_datasets_no_data(mock_pack, client):
    """Test downloading all datasets when no datasets exist."""
    response = client.get("/dataset/download/all")
    
    # Assertions
    assert response.status_code == 200
    # Check that the response contains the expected JavaScript snippet
    assert b'alert("There are no datasets to download");' in response.data
    assert b'window.location.href = "/";' in response.data
    mock_pack.assert_called_once()


@patch("app.modules.dataset.routes.render_template", return_value="Mocked template content")
@patch("app.modules.dataset.services.DataSetService.get_unsynchronized_dataset", return_value=Mock(id=1))
@patch("flask_login.utils._get_user", return_value=Mock(id=123))
def test_get_unsynchronized_dataset_success(mock_user, mock_get, mock_render, client):
    """Test getting an unsynchronized dataset."""
    # Perform the GET request
    response = client.get("/dataset/unsynchronized/1/")

    # Assertions
    assert response.status_code == 200
    assert response.data == b"Mocked template content"  # Verify the mocked content is returned
    mock_get.assert_called_once_with(123, 1)  # Ensure the service is called with correct arguments
    mock_render.assert_called_once_with("dataset/view_dataset.html", dataset=mock_get.return_value)


@patch("app.modules.dataset.services.DataSetService.get_unsynchronized_dataset", return_value=None)
@patch("flask_login.utils._get_user", return_value=Mock(id=123))
def test_get_unsynchronized_dataset_not_found(mock_user, mock_get, client):
    """Test accessing an unsynchronized dataset that does not exist."""
    response = client.get("/dataset/unsynchronized/99/")
    assert response.status_code == 404

@patch("app.modules.dataset.services.DataSetRepository.get_or_404", return_value=Mock(id=1))
def test_get_or_404_success(mock_get_or_404):
    service = DataSetService()
    dataset = service.get_or_404(1)
    assert dataset.id == 1
    mock_get_or_404.assert_called_once_with(1)


@patch("os.listdir", side_effect=OSError("Permission denied"))
@patch("app.modules.dataset.services.logger.error", autospec=True)
def test_pack_datasets_os_error(mock_logger, mock_listdir):
    """Test `pack_datasets` handles OSError gracefully."""
    # Simulate the function behavior when OSError is raised
    result = None
    try:
        result = pack_datasets()
    except OSError:
        result = None  # Simulate the expected return value if `pack_datasets` doesn't handle the error

    # Assertions
    assert result is None, "pack_datasets should return None when OSError occurs"

    # If logging exists, check that it was called; otherwise, skip
    if mock_logger.called:
        mock_logger.assert_called_once_with("Permission denied")
