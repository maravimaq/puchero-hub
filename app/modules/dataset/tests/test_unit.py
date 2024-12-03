import tempfile
from unittest.mock import mock_open, patch
import pytest
from app import db
from app.modules.auth.models import User
from app.modules.dataset.models import DataSet, DSMetaData, PublicationType
from app.modules.dataset.services import DataSetService
from app.modules.dataset.services import convert_uvl_to_cnf, convert_uvl_to_json, convert_uvl_to_splx, pack_datasets
from app.modules.dataset.services import convert_uvl_to_pdf
from unittest.mock import MagicMock

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


def test_pack_datasets_no_user_folders():
    with patch("os.path.exists", return_value=True), \
         patch("os.listdir", return_value=[]):
        result = pack_datasets()
        assert result is None


def test_pack_datasets_no_datasets_in_user_folder():
    with patch("os.path.exists", return_value=True), \
         patch("os.listdir", side_effect=[["user_1"], []]):
        result = pack_datasets()
        assert result is None


def test_pack_datasets_valid_files():
    mock_stat_result = MagicMock()
    with patch("app.modules.dataset.services.os.path.exists", return_value=True), \
         patch("app.modules.dataset.services.os.listdir", side_effect=[["user_1"], ["dataset_1"], ["file1.uvl"]]), \
         patch("app.modules.dataset.services.os.walk",
               return_value=[("uploads/user_1/dataset_1", [], ["file1.uvl"])]), \
         patch("app.modules.dataset.services.tempfile.mkdtemp", return_value=tempfile.gettempdir()), \
         patch("app.modules.dataset.services.os.path.isdir", side_effect=lambda path: "dataset_1" in path), \
         patch("app.modules.dataset.services.os.stat", return_value=mock_stat_result), \
         patch("app.modules.dataset.services.convert_uvl_to_pdf"), \
         patch("app.modules.dataset.services.convert_uvl_to_json"), \
         patch("app.modules.dataset.services.convert_uvl_to_cnf"), \
         patch("app.modules.dataset.services.convert_uvl_to_splx"):

        result = dataset_service.pack_datasets()
        assert result is not None
        assert result.endswith(".zip")


def test_pack_datasets_no_valid_files():
    with patch("os.path.exists", return_value=True), \
         patch("os.listdir", side_effect=[["user_1"], ["dataset_1"], []]), \
         patch("os.walk", return_value=[]), \
         patch("tempfile.mkdtemp", return_value=tempfile.gettempdir()), \
         patch("os.path.isdir", return_value=True):

        result = pack_datasets()
        assert result is None


def test_convert_uvl_to_pdf_success():
    uvl_content = "This is a test UVL file."
    mock_pdf_output = "/path/to/output.pdf"

    with patch("builtins.open", mock_open(read_data=uvl_content)), \
         patch("app.modules.dataset.services.FPDF") as MockPDF:
        mock_pdf = MockPDF.return_value
        mock_pdf.output.return_value = None

        convert_uvl_to_pdf("/path/to/input.uvl", mock_pdf_output)

        MockPDF.assert_called_once()
        mock_pdf.add_page.assert_called_once()
        mock_pdf.set_font.assert_called_once_with("Arial", size=12)
        mock_pdf.multi_cell.assert_called_once_with(0, 10, uvl_content)
        mock_pdf.output.assert_called_once_with(mock_pdf_output)


def test_convert_uvl_to_pdf_empty_file():
    with patch("builtins.open", mock_open(read_data="")), \
         patch("app.modules.dataset.services.FPDF"), \
         patch("builtins.print") as mock_print:
        convert_uvl_to_pdf("/path/to/input.uvl", "/path/to/output.pdf")
        mock_print.assert_called_once_with(
            "Error al convertir /path/to/input.uvl a PDF: El archivo /path/to/input.uvl está vacío."
        )


def test_convert_uvl_to_pdf_exception():
    with patch("builtins.open", mock_open(read_data="data")), \
         patch("app.modules.dataset.services.FPDF") as MockPDF:
        MockPDF.side_effect = Exception("PDF generation failed")

        with patch("builtins.print") as mock_print:
            convert_uvl_to_pdf("/path/to/input.uvl", "/path/to/output.pdf")
            mock_print.assert_called_once_with(
                "Error al convertir /path/to/input.uvl a PDF: PDF generation failed"
            )


def test_convert_uvl_to_json_success():
    uvl_content = "This is a test UVL file."
    expected_json = {"data": uvl_content}

    mock_uvl_file = mock_open(read_data=uvl_content)
    mock_json_file = mock_open()

    with patch("builtins.open", mock_uvl_file) as mocked_open:
        mocked_open.side_effect = [mock_uvl_file.return_value, mock_json_file.return_value]
        with patch("json.dump") as mock_json_dump:
            convert_uvl_to_json("/path/to/input.uvl", "/path/to/output.json")
            mocked_open.assert_any_call("/path/to/input.uvl", "r")
            mocked_open.assert_any_call("/path/to/output.json", "w")
            mock_json_dump.assert_called_once_with(expected_json, mock_json_file(), indent=4)


def test_convert_uvl_to_json_empty_file():
    with patch("builtins.open", mock_open(read_data="")), \
         patch("json.dump"), \
         patch("builtins.print") as mock_print:
        convert_uvl_to_json("/path/to/input.uvl", "/path/to/output.json")
        mock_print.assert_called_once_with(
            "Error al convertir /path/to/input.uvl a JSON: El archivo /path/to/input.uvl está vacío."
        )


def test_convert_uvl_to_json_exception():
    with patch("builtins.open", mock_open(read_data="data")), \
         patch("json.dump") as mock_json_dump:
        mock_json_dump.side_effect = Exception("JSON writing failed")

        with patch("builtins.print") as mock_print:
            convert_uvl_to_json("/path/to/input.uvl", "/path/to/output.json")
            mock_print.assert_called_once_with(
                "Error al convertir /path/to/input.uvl a JSON: JSON writing failed"
            )


def test_convert_uvl_to_cnf_success():
    uvl_content = "Line 1\nLine 2\n"
    with patch("builtins.open", mock_open(read_data=uvl_content)) as mock_file:
        convert_uvl_to_cnf("/path/to/input.uvl", "/path/to/output.cnf")

        mock_file.assert_called_with("/path/to/output.cnf", "w")
        mock_file().write.assert_any_call("Line 1\n")
        mock_file().write.assert_any_call("Line 2\n")


def test_convert_uvl_to_cnf_empty_file():
    with patch("builtins.open", mock_open(read_data="")), \
         patch("builtins.print") as mock_print:
        convert_uvl_to_cnf("/path/to/input.uvl", "/path/to/output.cnf")
        mock_print.assert_called_once_with(
            "Error al convertir /path/to/input.uvl a CNF: El archivo /path/to/input.uvl está vacío."
        )


def test_convert_uvl_to_cnf_exception():
    with patch("builtins.open", mock_open(read_data="data")) as mock_file:
        mock_file.side_effect = Exception("CNF writing failed")

        with patch("builtins.print") as mock_print:
            convert_uvl_to_cnf("/path/to/input.uvl", "/path/to/output.cnf")
            mock_print.assert_called_once_with(
                "Error al convertir /path/to/input.uvl a CNF: CNF writing failed"
            )


def test_convert_uvl_to_splx_success():
    uvl_content = "Line 1\nLine 2\n"
    with patch("builtins.open", mock_open(read_data=uvl_content)) as mock_file:
        convert_uvl_to_splx("/path/to/input.uvl", "/path/to/output.splx")

        mock_file.assert_called_with("/path/to/output.splx", "w")
        mock_file().write.assert_any_call("Line 1\n")
        mock_file().write.assert_any_call("Line 2\n")


def test_convert_uvl_to_splx_empty_file():
    with patch("builtins.open", mock_open(read_data="")), \
         patch("builtins.print") as mock_print:
        convert_uvl_to_splx("/path/to/input.uvl", "/path/to/output.splx")
        mock_print.assert_called_once_with(
            "Error al convertir /path/to/input.uvl a SPLX: El archivo /path/to/input.uvl está vacío."
        )


def test_convert_uvl_to_splx_exception():
    with patch("builtins.open", mock_open(read_data="data")), \
         patch("builtins.open") as mock_write_file:
        mock_write_file.side_effect = Exception("SPLX writing failed")

        with patch("builtins.print") as mock_print:
            convert_uvl_to_splx("/path/to/input.uvl", "/path/to/output.splx")
            mock_print.assert_called_once_with(
                "Error al convertir /path/to/input.uvl a SPLX: SPLX writing failed"
            )
