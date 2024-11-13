import logging
from flask import jsonify, Response
from app.modules.fakenodo.repositories import FakenodoRepository
from core.services.BaseService import BaseService
logger = logging.getLogger(__name__)


class FakenodoService(BaseService):
    def __init__(self):
        super().__init__(FakenodoRepository())
        self.headers = {"Content-Type": "application/json"}
        self.mock_data = {}
        self.next_id = 1

    def test_connection(self) -> bool:

        logger.info("Simulated connection to Fakenodo API successful.")
        return True

    def test_full_connection(self) -> Response:

        deposition = self.create_new_deposition({"title": "Test Deposition", "description": "Mock description"})
        deposition_id = deposition["id"]
        self.upload_file(deposition_id, {"filename": "test_file.txt", "content": "Fake file content"})
        self.delete_deposition(deposition_id)
        return jsonify({"success": True, "message": "Full connection test passed with Fakenodo mock API."})

    def get_all_depositions(self) -> dict:

        return {"depositions": list(self.mock_data.values())}

    def create_new_deposition(self, metadata) -> dict:

        deposition_id = self.next_id
        self.next_id += 1
        deposition = {
            "id": deposition_id,
            "title": metadata.get("title", "Untitled"),
            "description": metadata.get("description", ""),
            "status": "draft"
        }
        self.mock_data[deposition_id] = deposition
        logger.info(f"Created new mock deposition: {deposition}")
        return deposition

    def upload_file(self, deposition_id, file_data) -> dict:

        if deposition_id not in self.mock_data:
            raise Exception("Deposition not found")
        file_info = {
            "filename": file_data.get("filename", "untitled.txt"),
            "status": "uploaded"
        }
        self.mock_data[deposition_id].update({"file": file_info})
        logger.info(f"Uploaded mock file to deposition {deposition_id}")
        return file_info

    def publish_deposition(self, deposition_id: int) -> dict:

        if deposition_id not in self.mock_data:
            raise Exception("Deposition not found")
        self.mock_data[deposition_id]["status"] = "published"
        logger.info(f"Published mock deposition with ID {deposition_id}")
        return self.mock_data[deposition_id]

    def get_deposition(self, deposition_id: int) -> dict:

        if deposition_id not in self.mock_data:
            raise Exception("Deposition not found")
        return self.mock_data[deposition_id]

    def delete_deposition(self, deposition_id: int) -> dict:

        if deposition_id in self.mock_data:
            del self.mock_data[deposition_id]
            logger.info(f"Deleted mock deposition with ID {deposition_id}")
            return {"id": deposition_id, "status": "deleted"}
        raise Exception("Deposition not found")

    def get_doi(self, deposition_id: int) -> str:

        return f"10.1234/fake-doi-{deposition_id}"
