from locust import HttpUser, TaskSet, between, task
from core.locust.common import get_csrf_token
from core.environment.host import get_host_for_locust_testing


class ProfileBehavior(TaskSet):
    """Simula las acciones del módulo 'profile'."""

    def on_start(self):
        """Acciones al iniciar el test: iniciar sesión."""
        self.login()

    @task(2)
    def view_profile_summary(self):
        """Carga el resumen del perfil del usuario autenticado."""
        with self.client.get("/profile/summary", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error al cargar perfil: {response.status_code}")

    @task(1)
    def edit_profile(self):
        """Simula la edición del perfil del usuario."""
        # Obtener el token CSRF
        response = self.client.get("/profile/edit")
        csrf_token = get_csrf_token(response)
        if not csrf_token:
            response.failure("No se pudo obtener el token CSRF para editar el perfil.")
            return

        # Enviar el formulario de edición del perfil
        form_data = {
            "name": "Test User",
            "surname": "Updated",
            "email": "testuser@example.com",
            "csrf_token": csrf_token,
        }
        with self.client.post("/profile/edit", data=form_data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error al editar el perfil: {response.status_code}")

    @task(2)
    def view_public_profile(self):
        """Carga el perfil público de un usuario específico."""
        user_id = 2
        with self.client.get(f"/public_profile/{user_id}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error al cargar perfil público: {response.status_code}")

    def login(self):
        """Simula el inicio de sesión del usuario."""
        response = self.client.get("/login")
        csrf_token = get_csrf_token(response)
        if not csrf_token:
            response.failure("No se pudo obtener el token CSRF para el inicio de sesión.")
            return

        login_data = {
            "email": "testuser@example.com",
            "password": "test1234",
            "csrf_token": csrf_token,
        }
        with self.client.post("/login", data=login_data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error al iniciar sesión: {response.status_code}")


class ProfileUser(HttpUser):
    """Clase principal que define el usuario de Locust para el módulo 'profile'."""
    tasks = [ProfileBehavior]
    wait_time = between(1, 5)
    host = get_host_for_locust_testing()
