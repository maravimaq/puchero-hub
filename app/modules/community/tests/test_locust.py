from secrets import randbelow
from locust import HttpUser, task, between


class CommunityUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.client.post("/login", data={
            "email": "testuser@example.com",
            "password": "test1234"
        })

    @task(2)
    def view_my_communities(self):
        with self.client.get("/my-communities", catch_response=True) as response:
            if response.status_code == 200:
                print("Lista de comunidades cargada exitosamente.")
            else:
                print(f"Error al cargar las comunidades: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def create_community(self):
        new_community = {
            "name": f"Community Locust {randbelow(100000)}",
            "description": "Test community created during load testing."
        }
        with self.client.post("/community/create", data=new_community, catch_response=True) as response:
            if response.status_code == 200:
                print("Comunidad creada exitosamente.")
            else:
                print(f"Error al crear la comunidad: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def edit_community(self):
        community_id = randbelow(100000)
        updated_data = {
            "name": f"Updated Community {community_id}",
            "description": "Updated description for load testing."
        }
        with self.client.post(f"/community/edit/{community_id}", data=updated_data, catch_response=True) as response:
            if response.status_code == 200:
                print(f"Comunidad {community_id} editada exitosamente.")
            else:
                print(f"Error al editar la comunidad {community_id}: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def delete_community(self):
        community_id = randbelow(100000)
        with self.client.post(f"/community/delete/{community_id}", catch_response=True) as response:
            if response.status_code == 200:
                print(f"Comunidad {community_id} eliminada exitosamente.")
            else:
                print(f"Error al eliminar la comunidad {community_id}: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def view_specific_community(self):
        community_id = randbelow(100000)
        with self.client.get(f"/community/{community_id}", catch_response=True) as response:
            if response.status_code == 200:
                print(f"Detalles de la comunidad {community_id} cargados exitosamente.")
            else:
                print(f"Error al cargar la comunidad {community_id}: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def view_not_joined_communities(self):
        with self.client.get("/communities/not-joined", catch_response=True) as response:
            if response.status_code == 200:
                print("Lista de comunidades no unidas cargada exitosamente.")
            else:
                print(f"Error al cargar comunidades no unidas: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def join_community(self):
        community_id = randbelow(100000)
        with self.client.post(f"/community/join/{community_id}", catch_response=True) as response:
            if response.status_code == 200:
                print(f"Unido a la comunidad {community_id} exitosamente.")
            else:
                print(f"Error al unirse a la comunidad {community_id}: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    def on_stop(self):
        self.client.get("/logout")
