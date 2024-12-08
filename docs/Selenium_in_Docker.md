
# Configuración de Selenium en Docker

Esta guía describe los pasos necesarios para configurar y ejecutar pruebas de Selenium en un entorno Dockerizado.

---

## **Pasos para Configurar Selenium en Docker**

### 1. Antes de continuar, ejecuta el script de limpieza para asegurarte de que la configuración funcione correctamente. 
Este paso debe repetirse cada vez que se cambie de rama:

   ```bash
   sudo scripts/clean_docker.sh sh
```

### **2. Ejecutar los contenedores**

Ejecuta los contenedores necesarios utilizando el siguiente comando:
```bash
docker compose -f docker/docker-compose.dev.yml up -d
```

### **3. Acceder al contenedor**

Accede al contenedor de tu aplicación web:
```
sudo docker exec -it web_app_container bash
```

### **4. Instalar navegador**

Descarga e instala manualmente Google Chrome:
```bash
apt update
apt install -y chromium
curl -o google-chrome-stable.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable.deb
apt-get -f install  # Corrige dependencias
```
Verifica la instalación de Google Chrome:
```bash
google-chrome --version
# Salida esperada: Google Chrome 131.0.6778.108
```

### **5. Instalar ChromeDriver**

Instala manualmente una versión compatible de ChromeDriver:

1. Descarga la versión específica de ChromeDriver que coincida con la versión de Chrome instalada:
    ```bash
    apt-get update
    apt-get install -y chromium-driver
    ```

3. Verifica la instalación de ChromeDriver:
    ```bash
    chromedriver --version
    # Salida esperada: ChromeDriver 131.0.6778.108
    ```

### **6. Actualizar la Configuración de Pruebas de Selenium**

Modifica los tests de Selenium para que utilicen la configuración adecuada:

1. Asegúrate de que el `Service` apunte al ChromeDriver instalado manualmente en `/usr/bin/chromedriver`.

2. Añade opciones de Chrome para ejecutar en un entorno sin interfaz gráfica (headless).

Ejemplo de configuración:
```python
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/chromedriver")
self.driver = webdriver.Chrome(service=service, options=options)
```

### **7. Corregir la URL Base**

Reemplaza las referencias a `http://localhost/` en los tests por `http://web_app_container:5000/` para que coincidan con el entorno Dockerizado.

Ejemplo:
```python
# Antes:
self.driver.get("http://localhost/")

# Después:
self.driver.get("http://web_app_container:5000/")
```

### **8. Verificar las Pruebas de Selenium**

Ejecuta las pruebas para confirmar que funcionan correctamente:
```bash
rosemary selenium
```

---

## **Resumen de Software Instalado**

- **Google Chrome**: 131.0.6778.108

- **ChromeDriver**: 131.0.6778.108

---

## **Consejos para Solucionar Problemas**

### **Error: ERR_CONNECTION_REFUSED**

- Verifica que la aplicación web esté ejecutándose y accesible en `http://web_app_container:5000/`.

### **Incompatibilidad entre versiones de Chrome y ChromeDriver**

- Asegúrate de que las versiones de ChromeDriver y Google Chrome coincidan. Consulta la [tabla de compatibilidad de ChromeDriver](https://chromedriver.chromium.org/downloads).

### **Dependencias faltantes**

- Usa el siguiente comando para resolver dependencias faltantes después de instalar Google Chrome:

    ```bash
    apt-get -f install
    ```
