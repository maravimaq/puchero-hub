# Documentación de Scripts

## Script: `setup_selenium_docker.sh`

### Propósito

El script `setup_selenium_docker.sh` automatiza el proceso de limpieza, configuración e instalación de dependencias en un entorno Docker para el contenedor de la aplicación web.

### Ubicación esperada

`/scripts/setup_selenium_docker.sh`

---

### Funcionamiento paso a paso

1. **Limpieza de Docker**  
   Ejecuta un script de limpieza para eliminar contenedores y recursos no utilizados antes de iniciar nuevos servicios.

2. **Inicio de contenedores con Docker Compose**  
   Levanta los servicios definidos en el archivo `docker-compose.dev.yml` en modo detached (`-d`).

3. **Instalación de herramientas y dependencias en el contenedor**  
   Ejecuta comandos dentro del contenedor para instalar herramientas como `chromium`, `google-chrome` y `chromium-driver`, necesarias para el entorno de trabajo.

4. **Verificación de errores**  
   El script incluye comprobaciones en cada paso crítico, saliendo con un mensaje de error claro si algo falla.

---

### Código del script

```bash
#!/bin/bash

# Constants
DOCKER_COMPOSE_FILE="docker/docker-compose.dev.yml"
WEB_APP_CONTAINER_NAME="web_app_container"

# Step 1: Clean Docker
echo "Running Docker cleanup script..."
sudo scripts/clean_docker.sh sh

# Step 2: Start Docker Compose
echo "Starting Docker containers with docker-compose..."
docker compose -f $DOCKER_COMPOSE_FILE up -d
if [ $? -ne 0 ]; then
    echo "Error: Failed to start Docker containers."
    exit 1
fi

# Step 3: Execute setup commands in the container
echo "Running setup commands inside the web application container..."
sudo docker exec -i $WEB_APP_CONTAINER_NAME bash -c "
    apt update && \
    apt install -y chromium && \
    curl -o google-chrome-stable.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable.deb || apt-get -f install -y && \
    apt-get update && \
    apt-get install -y chromium-driver
"

if [ $? -ne 0 ]; then
    echo "Error: Failed to execute setup commands in the container."
    exit 1
fi

echo "Setup completed successfully!"
