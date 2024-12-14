# Workflow: Actualización del Badge de Cobertura

## Propósito

Actualizar automáticamente el badge de cobertura de código en cada *push* o *pull request* hacia la rama principal.

---

## Activadores del Workflow

El workflow se activa en los siguientes eventos:

- **Push**:
  - Ramas: `main`
- **Pull Request**:
  - Ramas: `main`

---

## Configuración de Permisos

```yaml
permissions:
  contents: write
```

---

## Descripción de los Jobs

### Job: `update-coverage`

El workflow define un único job llamado `update-coverage`, que se encarga de realizar todas las tareas necesarias para actualizar el badge de cobertura de código.

---

#### 1. Configuración del Entorno

Este job utiliza el sistema operativo Ubuntu en su versión más reciente y configura un servicio adicional de base de datos MySQL versión `5.7`. La configuración de MySQL incluye variables de entorno, puertos y opciones para la verificación de la salud del servicio.

```yaml
jobs:
  update-coverage:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:5.7
        env:
          MYSQL_ROOT_PASSWORD: uvlhub_root_password
          MYSQL_DATABASE: uvlhubdb_test
          MYSQL_USER: uvlhub_user
          MYSQL_PASSWORD: uvlhub_password
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3
```

---

#### 2. Pasos del Job

Este apartado detalla los pasos necesarios para ejecutar el job `update-coverage` y actualizar el badge de cobertura.

---

**Paso 1: Checkout del Código**

Clona el código del repositorio completo para garantizar el acceso a todas las ramas y el historial.

```yaml
- name: Checkout Code
  uses: actions/checkout@v4
  with:
    fetch-depth: 0
```

---

**Paso 2: Configurar Python**

Establece un entorno de Python utilizando la versión `3.12`, necesaria para ejecutar los tests y herramientas de cobertura.

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.12"
```

---

**Paso 3: Instalar Dependencias**

Actualiza `pip` e instala las dependencias necesarias desde el archivo `requirements.txt`.

```yaml
- name: Install Dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

---

**Paso 4: Ejecutar Pruebas y Generar Badge**

Ejecuta los tests del proyecto utilizando `pytest` y genera el badge de cobertura en formato SVG.

```yaml
- name: Run Tests and Generate Coverage Badge
  env:
    FLASK_ENV: testing
    MARIADB_HOSTNAME: 127.0.0.1
    MARIADB_PORT: 3306
    MARIADB_TEST_DATABASE: uvlhubdb_test
    MARIADB_USER: uvlhub_user
    MARIADB_PASSWORD: uvlhub_password
  run: |
    coverage run -m pytest app/modules/ --ignore-glob='*selenium*'
    rm -f coverage.svg
    coverage-badge -o coverage.svg
```

---

**Paso 5: Manejo de Conflictos y Commit del Badge**

Configura las credenciales para los commits, maneja posibles conflictos en el archivo `coverage.svg` y realiza el commit y push de los cambios.

```yaml
- name: Handle Conflicts and Commit Badge
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    git config --global user.name "GitHub Actions"
    git config --global user.email "actions@github.com"

    git stash push -m "Temporary stash for coverage badge changes" || echo "No changes to stash"

    if [ "${{ github.event_name }}" == "pull_request" ]; then
      echo "Pull request detected. Checking out the source branch: ${{ github.head_ref }}"
      git fetch origin ${{ github.head_ref }}:${{ github.head_ref }}
      git checkout ${{ github.head_ref }}
    else
      echo "Push event detected. Using branch: ${{ github.ref_name }}"
      git checkout ${{ github.ref_name }}
    fi

    git stash list | grep "Temporary stash for coverage badge changes" && git stash pop || echo "No stash to apply"

    if git ls-files -u | grep -q coverage.svg; then
      echo "Conflict detected in coverage.svg. Overwriting with generated file."
      cp coverage.svg coverage.resolved.svg
      mv coverage.resolved.svg coverage.svg
      git add coverage.svg
    fi

    git add coverage.svg
    git commit -m "Update coverage badge" || echo "No changes to commit"
    git push origin HEAD:${{ github.head_ref || github.ref_name }}
```

- **Detección de conflictos**: Identifica si existen conflictos en el archivo `coverage.svg` y los resuelve sobrescribiéndolo.
- **Commit y Push**: Sube los cambios a la rama correspondiente.

---

## Notas Adicionales

- Es necesario configurar el secreto `GITHUB_TOKEN` en el repositorio para autenticar los commits.
- Este workflow depende de herramientas como `coverage` y `coverage-badge`, que deben estar instaladas en el entorno Python.
