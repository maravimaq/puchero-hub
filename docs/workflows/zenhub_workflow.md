# Documentación del Workflow de Zenhub

## Descripción General

- **Nombre del Workflow**: `Zenhub Workflow`

- **Objetivo**: Actualizar las pipelines de Zenhub automáticamente cuando se crean, editan o cierran issues y pull requests en GitHub.

- **Eventos que disparan el workflow**:

  - **Issues**: `opened`, `edited`, `closed`

  - **Pull Requests**: `opened`, `closed`

---

## Explicación Paso a Paso del Workflow

Este workflow está diseñado para interactuar con Zenhub y actualizar automáticamente las pipelines en función de los eventos generados en GitHub. A continuación, se explica cada parte del código.

---

### Configuración del Workflow

```yaml
name: Zenhub Workflow
```

- **Propósito**: Establece el nombre del workflow, en este caso, `Zenhub Workflow`, para identificarlo en la lista de workflows de GitHub Actions.

---

### Eventos que Activan el Workflow

```yaml
on:
  issues:
    types: [opened, edited, closed]
  pull_request:
    types: [opened, closed]
```

- **`on`**: Define los eventos de GitHub que dispararán la ejecución del workflow.

- **`issues`**: Se activará cuando una issue sea:

  - `opened`: Creada.

  - `edited`: Editada.

  - `closed`: Cerrada.

- **`pull_request`**: Se activará cuando un pull request sea:

  - `opened`: Creado.

  - `closed`: Cerrado.

---

### Definición del Trabajo (`job`)

```yaml
jobs:
  update-zenhub:
    runs-on: ubuntu-latest
```

- **`jobs`**: Define los trabajos (jobs) que ejecutará el workflow.

- **`update-zenhub`**: Nombre del trabajo que realizará la actualización en Zenhub.

- **`runs-on: ubuntu-latest`**: Especifica que el trabajo se ejecutará en un runner con el sistema operativo Ubuntu en su versión más reciente.

---

### Pasos del Job

#### 1. Clonar el Código del Repositorio

```yaml
- name: Check out code
  uses: actions/checkout@v4
```

- **Propósito**: Clona el código del repositorio en el entorno del runner para que esté disponible durante la ejecución del workflow.

- **`uses`**: Utiliza la acción oficial `actions/checkout` en su versión 4.

---

#### 2. Configurar el Entorno de Python

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.12"
```

- **Propósito**: Configura un entorno de Python en el runner.

- **`uses`**: Utiliza la acción oficial `actions/setup-python` en su versión 5.

- **`python-version`**: Establece que se usará la versión 3.12 de Python.

---

#### 3. Instalar Dependencias

```yaml
- name: Install dependencies
  run: |
    python -m pip install requests
```

- **Propósito**: Instala la biblioteca `requests`, necesaria para realizar solicitudes HTTP a la API de Zenhub.

- **`run`**: Ejecuta un comando de instalación utilizando `pip`.

---

#### 4. Ejecutar el Script de Actualización

```yaml
- name: Update Zenhub Pipeline
  env:
    ZENHUB_API_TOKEN: ${{ secrets.ZENHUB_API_TOKEN }}
  run: |
    python - <<EOF
    # Código Python...
    EOF
```

- **Propósito**: Ejecuta un script de Python que interactúa con la API de Zenhub.

- **`env`**: 

  - **`ZENHUB_API_TOKEN`**: Usa un secreto configurado en GitHub para autenticar las solicitudes a la API de Zenhub.

- **`run`**: Ejecuta un bloque de código Python directamente desde el workflow.

---

### Código Python: Paso a Paso

#### 1. Configuración Inicial

```python
ZENHUB_API_URL = "https://api.zenhub.com/p1/repositories/{repo_id}/issues/{issue_number}/moves"
ZENHUB_TOKEN = os.getenv("ZENHUB_API_TOKEN")
REPO_ID = "871646266"  # ID del repositorio de GitHub
```

- Define la URL base para las solicitudes a la API de Zenhub.

- Obtiene el token de autenticación desde las variables de entorno.

- Especifica el ID del repositorio asociado.

---

#### 2. Definir Pipelines

```python
PIPELINES = {
    "new_issues": "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzMzODc2NzM",
    "in_progress": "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzMzODc2Nzc",
    "review_qa": "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzMzODc2Nzg",
    "done": "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzMzODc2Nzk"
}
```

- Asocia nombres legibles (como `new_issues`, `in_progress`) con los IDs de las pipelines en Zenhub.

---

#### 3. Validar el Evento

```python
ISSUE_NUMBER = os.getenv("ISSUE_NUMBER")
EVENT_NAME = os.getenv("GITHUB_EVENT_NAME")

if not ISSUE_NUMBER:
    print("No ISSUE_NUMBER provided. Skipping Zenhub update.")
    exit(0)
```

- Obtiene el número de la issue y el nombre del evento desde las variables de entorno.

- Si no se proporciona un número de issue, el script termina sin realizar ninguna acción.

---

#### 4. Determinar el Pipeline

```python
if EVENT_NAME == "issues" and os.getenv("GITHUB_EVENT_ACTION") == "opened":
    pipeline_id = PIPELINES["new_issues"]
elif EVENT_NAME == "pull_request" and os.getenv("GITHUB_EVENT_ACTION") == "opened":
    pipeline_id = PIPELINES["in_progress"]
elif EVENT_NAME == "pull_request" and os.getenv("GITHUB_EVENT_ACTION") == "closed":
    pipeline_id = PIPELINES["review_qa"]
elif EVENT_NAME == "issues" and os.getenv("GITHUB_EVENT_ACTION") == "closed":
    pipeline_id = PIPELINES["done"]
else:
    print("No matching pipeline for this event.")
    exit(0)
```

- Según el tipo de evento y acción, selecciona el ID del pipeline correspondiente:

  - `new_issues`: Para issues recién creadas.

  - `in_progress`: Para pull requests abiertos.

  - `review_qa`: Para pull requests cerrados.

  - `done`: Para issues cerradas.

---

#### 5. Realizar la Solicitud a la API

```python
headers = {
    "X-Authentication-Token": ZENHUB_TOKEN,
    "Content-Type": "application/json",
}

data = {
    "pipeline_id": pipeline_id,
    "position": "top"
}

response = requests.post(
    ZENHUB_API_URL.format(repo_id=REPO_ID, issue_number=ISSUE_NUMBER),
    json=data,
    headers=headers,
)

if response.status_code == 200:
    print(f"Issue #{ISSUE_NUMBER} successfully moved to pipeline {pipeline_id}.")
else:
    print(f"Failed to update issue #{ISSUE_NUMBER}: {response.status_code}, {response.text}")
```

- Configura los **headers** necesarios para la autenticación.

- Prepara los **datos** para especificar el pipeline y la posición.

- Realiza la solicitud POST a la API de Zenhub con la URL, datos y headers.

- Maneja la respuesta:

  - **Éxito**: Muestra un mensaje indicando que la issue fue movida exitosamente.

  - **Error**: Imprime el código de estado y el mensaje de error devuelto.

---
