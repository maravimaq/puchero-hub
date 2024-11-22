import pytest
from unittest.mock import patch, Mock, MagicMock, mock_open
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

# Mock the Flask app and SQLAlchemy for testing
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app


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

    # Assert the file was opened and written to
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

    # Assert the file was opened and written to
    mock_open.assert_any_call(input_file, "r")
    mock_open.assert_any_call(output_file, "w")
    handle = mock_open()
    handle.write.assert_any_call("Line 1\n")
    handle.write.assert_any_call("Line 2\n")


# Test pack_datasets
@patch("os.path.exists", return_value=True)
@patch("os.makedirs")
@patch("os.listdir", side_effect=[["user_1"], ["dataset_1"], ["file.uvl"]])
@patch("os.walk", return_value=[("dummy_path", [], ["file.uvl"])])
@patch("app.modules.dataset.services.ZipFile")
@patch("app.modules.dataset.services.convert_uvl_to_pdf")
@patch("os.remove")
def test_pack_datasets(mock_remove, mock_convert_pdf, mock_zipfile, mock_walk, mock_listdir, mock_makedirs, mock_exists):
    mock_zip_instance = MagicMock()
    mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

    result = pack_datasets()

    assert result is not None
    mock_zip_instance.write.assert_called()
    mock_convert_pdf.assert_called()
    mock_remove.assert_called()


# Test DataSetService.get_synchronized
@patch("app.modules.dataset.services.DataSetRepository")
def test_get_synchronized(mock_ds_repo):
    mock_ds_repo.return_value.get_synchronized.return_value = "mock_dataset"
    service = DataSetService()
    result = service.get_synchronized(1)
    assert result == "mock_dataset"
    mock_ds_repo.return_value.get_synchronized.assert_called_once_with(1)
