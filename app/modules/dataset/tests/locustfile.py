from locust import HttpUser, TaskSet, between, task
from core.locust.common import get_csrf_token
from core.environment.host import get_host_for_locust_testing


class UploadDatasetBehavior(TaskSet):
    """Handles tasks related to uploading datasets."""

    def on_start(self):
        """Simulate login or any required setup before starting."""
        self.login()

    @task(2)
    def upload_dataset(self):
        """Simulate dataset upload."""
        response = self.client.get("/dataset/upload")
        csrf_token = get_csrf_token(response)

        form_data = {
            "name": "Test Dataset",
            "description": "This is a test dataset",
            "file": ("test_file.uvl", "UVL file content here"),
        }
        headers = {"X-CSRFToken": csrf_token}
        response = self.client.post("/dataset/upload", data=form_data, headers=headers)
        if response.status_code == 200:
            response.success()
        else:
            response.failure("Dataset upload failed")

    def login(self):
        """Simulate login to access protected routes."""
        response = self.client.get("/login")
        csrf_token = get_csrf_token(response)
        if csrf_token:
            login_data = {
                "username": "user@example.com",
                "password": "password",
                "csrf_token": csrf_token,
            }
            response = self.client.post("/login", data=login_data)
            if response.status_code != 200:
                response.failure("Login failed")


class ListAndViewDatasetBehavior(TaskSet):
    """Handles listing and viewing datasets."""

    def on_start(self):
        """Simulate login or any required setup before starting."""
        self.login()

    @task(2)
    def list_datasets(self):
        """Simulate listing datasets."""
        response = self.client.get("/dataset/list")
        if response.status_code == 200:
            response.success()
        else:
            response.failure("Failed to list datasets")

    @task(1)
    def view_unsynchronized_dataset(self):
        """Simulate viewing an unsynchronized dataset."""
        dataset_id = 1  # Replace with an actual dataset ID
        response = self.client.get(f"/dataset/unsynchronized/{dataset_id}/")
        if response.status_code == 200:
            response.success()
        else:
            response.failure(f"Failed to view unsynchronized dataset: {response.status_code}")

    def login(self):
        """Simulate login to access protected routes."""
        response = self.client.get("/login")
        csrf_token = get_csrf_token(response)
        if csrf_token:
            login_data = {
                "username": "user@example.com",
                "password": "password",
                "csrf_token": csrf_token,
            }
            response = self.client.post("/login", data=login_data)
            if response.status_code != 200:
                response.failure("Login failed")


class DatasetUser(HttpUser):
    """Main user class to simulate dataset-related actions."""
    tasks = [UploadDatasetBehavior, ListAndViewDatasetBehavior]
    wait_time = between(5, 9)
    host = get_host_for_locust_testing()
