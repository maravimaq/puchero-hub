from locust import HttpUser, TaskSet, task, between
from core.locust.common import get_csrf_token
from core.environment.host import get_host_for_locust_testing
import json as JSON


class ExploreBehavior(TaskSet):
    """Simula las acciones del módulo 'explore'."""

    def on_start(self):
        """Simulate login or any required setup before starting."""
        self.login()

    @task(3)
    def search_datasets(self):
        """Simula la búsqueda de datasets."""
        response = self.client.get("/explore")
        csrf_token = get_csrf_token(response)

        search_criteria = {
            "title": "Sample",
            "author": "Author",
            "tags": "tag1",
            "publication_doi": "10.1234",
            "description": "Description",
            "size_from": "0",
            "size_to": "10",
            "sorting": "newest",
        }
        headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        }
        with self.client.post("/explore", data=JSON.dumps(search_criteria), headers=headers,
                              catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error al buscar datasets: {response.status_code}")

    def login(self):
        """Simulate login to access protected routes."""
        response = self.client.get("/login")
        csrf_token = get_csrf_token(response)
        if csrf_token:
            login_data = {
                "username": "user1@example.com",
                "password": "1234",
                "csrf_token": csrf_token,
            }
            response = self.client.post("/login", data=login_data)
            if response.status_code != 200:
                response.failure("Login failed")


class ExploreUser(HttpUser):
    """Clase principal que define el usuario de Locust para el módulo 'explore'."""
    tasks = [ExploreBehavior]
    wait_time = between(5, 9)
    host = get_host_for_locust_testing()
