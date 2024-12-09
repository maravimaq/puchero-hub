
# Documentación de los fallos arreglados en los tests de Locust para Community

## Problemática general

Los tests de Locust para las rutas de comunidades no se ejecutaban correctamente desde Docker al ejecutar el comando `rosemary locust community`. Esto se debía a la falta de una definición explícita del `host` y a la estructura del archivo que no cumplía con los requisitos de Locust para identificar los tests.

---

## Solución aplicada

### 1. **Definir el host explícitamente**

#### Alcance del problema

Al abrir la interfaz de Locust, el campo `Host` aparecía vacío, lo que causaba que los tests no pudieran ejecutarse sin intervención manual. Esto sucedía porque el atributo `host` no estaba definido en la clase `CommunityUser`.

#### Corrección aplicada

Se añadió el atributo `host` en la clase `CommunityUser` utilizando la función `get_host_for_locust_testing()`, consistente con otros tests de Locust:

```python
from core.environment.host import get_host_for_locust_testing

class CommunityUser(HttpUser):
    wait_time = between(1, 5)
    host = get_host_for_locust_testing()  # Se define el host dinámicamente.
```

#### Estado después de la corrección

El campo `Host` en la interfaz de Locust ahora se llena automáticamente con el valor correcto (`http://nginx_web_server_container`), permitiendo ejecutar los tests sin configuración manual adicional.

---

### 2. **Cambiar el archivo de tests a `locustfile.py`**

#### Alcance del problema

Los tests de Locust estaban definidos en un archivo llamado `test_locust.py`. Locust busca por defecto un archivo llamado `locustfile.py`, por lo que no identificaba los tests correctamente al ejecutarse con Docker.

#### Corrección aplicada

Se renombró el archivo de `test_locust.py` a `locustfile.py` para cumplir con las convenciones de Locust.

```bash
mv test_locust.py locustfile.py
```

#### Estado después de la corrección

Locust ahora reconoce automáticamente los tests al ejecutar el comando `rosemary locust community`, y no es necesario especificar un archivo explícitamente.

---

## Pasos seguidos para resolver los fallos

1. **Identificar el alcance del problema**

   - Se verificó por qué el host estaba vacío en la interfaz.

   - Se investigó por qué Locust no ejecutaba los tests desde Docker.

2. **Definir el host dinámicamente**

   - Se añadió `host = get_host_for_locust_testing()` a la clase `CommunityUser`.

3. **Renombrar el archivo de tests**

   - Se renombró el archivo de `test_locust.py` a `locustfile.py` para cumplir con los requisitos de Locust.

4. **Probar la solución localmente**

   - Se ejecutó Locust localmente y desde Docker para verificar que los tests se detectaban correctamente y se llenaba el campo `Host`.

5. **Validar la solución con Docker**

   - Se ejecutó `rosemary locust community` y se comprobó que los tests funcionaban como se esperaba.

6. **Hacer commit y push de los cambios**

   - Se creó una nueva rama para los cambios y se realizó un commit con la solución.

7. **Crear un Pull Request**

   - Se abrió un Pull Request detallando los cambios realizados.

8. **Verificar tras el merge**

   - Se verificó que los cambios solucionaran los problemas en la rama `main`.

---

## Estado final

Con estas correcciones, los tests de Locust para las rutas de comunidades ahora se ejecutan correctamente desde Docker y no requieren configuración manual del `host`. La solución asegura que los tests sean detectados automáticamente por Locust al cumplir con las convenciones establecidas.
