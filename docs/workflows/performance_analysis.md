# Workflow: Actualización del Badge de Cobertura

## Propósito

Este workflow genera un documento en formato markdown que evalúa y clasifica el desempeño de los contribuidores del proyecto basado en métricas predefinidas. Estas métricas incluyen commits, issues cerradas, pull requests, workflows y tests realizados durante el ciclo de vida del proyecto. El resultado se presenta en una tabla detallada.

---

## Activadores del Workflow

El workflow se activa en los siguientes eventos:

- **Ejecución manual**:
  - Desde GitHub Actions se puede ejecutar manualmente.
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

### Job: `analyze-performance`

Este workflow define un único job llamado `analyze-performance`, que se encarga de procesar los datos de los contribuidores, calcular las métricas y generar un documento con los resultados.

---

#### 1. Configuración del Entorno

El job utiliza un entorno basado en Ubuntu y se asegura de tener acceso al código fuente del repositorio y a las herramientas necesarias para analizar los datos.

```yaml
jobs:
  update-coverage:
    runs-on: ubuntu-latest
```

---

#### 2. Pasos del Job

Este apartado detalla los pasos necesarios para ejecutar el job `analyze-performance` y actualizar la tabla de desempeño.

---

**Paso 1: Checkout del Código**

Clona el código del repositorio completo para garantizar el acceso a todos los archivos, incluidas las configuraciones y los historiales de commits.

```yaml
steps:
  - name: Checkout Code
    uses: actions/checkout@v4
    with:
      fetch-depth: 0
```

---

**Paso 2: Configurar Python**

Establece un entorno Python utilizando la versión `3.12`, necesario para ejecutar el script de análisis.

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.12"
```

---

**Paso 3: Instalar Dependencias**

Instala las dependencias necesarias para el análisis, incluyendo `requests` y `PyGithub`.

```yaml
- name: Install Dependencies
  run: pip install requests PyGithub
```

---

**Paso 4: Análisis del Desempeño de los Contribuidores**

El script en Python realiza las siguientes acciones:

- Definición de contribuidores válidos: Solo se evalúan los usuarios especificados: `pabmejbui`, `juanjunobr`, `maravimaq` y `julsolalf`.

- Procesamiento de métricas:

    - Commits: Se calcula el total de commits por contribuidor desde una fecha de inicio (1 de noviembre de 2023).
        - Se calcula una nota basada en la relación del número de commits del usuario con el promedio general.
    - Issues creadas: Se cuentan las issues cerradas por cada contribuidor.
        - La nota se basa en la relación entre el número de issues cerradas y la media general.
    - Pull requests: Se evalúan los pull requests cerrados y mergeados por contribuidor.
        - La nota se calcula en proporción a la actividad.
    - Workflows: Se verifica si el contribuidor ha modificado algún archivo en .github/workflows.
        - Nota fija: 10 si se ha creado algún workflow, 0 si no.
    - Tests realizados:
        - Se analizan los commits para identificar archivos de test creados (unitarios, integración, selenium y locust).
        - La nota depende del número de tipos de tests realizados:
            - 10: Todos los tipos.
            - 5: Tres tipos.
            - 2: Dos tipos.
            - 1: Un tipo.
            - 0: Ningún tipo.

- Generación del archivo markdown: Se genera un documento en docs/contributor_performance.md con una tabla detallada que incluye:

    - Contribuidor: Nombre de usuario.
    - Commits y Nota: Número de commits y la nota asignada.
    - Issues creadas y Nota.
    - Pull requests y Nota.
    - Workflows y Nota.
    - Tests y Nota.
    - Nota final: Promedio ponderado de las métricas.

```yaml
- name: Analyze Contributor Performance
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    python <<EOF
    # Código Python para el análisis
    EOF
```

---

**Paso 5: Commit y Push del Resultado**

El archivo generado se agrega al repositorio, y se realiza un commit con un mensaje descriptivo. En caso de no haber cambios, se omite el commit.

```yaml
- name: Commit and Push Results
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    git config user.name "GitHub Actions"
    git config user.email "actions@github.com"
    git add docs/contributor_performance.md
    git commit -m "docs(performance_workflow): Add contributor performance analysis" || echo "No changes to commit"
    git push origin ${{ github.head_ref }}
```

---

## Detalles de las Métricas
Las métricas y sus ponderaciones son:

    1. Commits (20%):
        - Se compara el número de commits del usuario con la media general.
        - Fórmula: (commits_usuario / media_commits) * 10.

    2. Issues creadas (20%):
        - Similar a los commits, la nota depende de la relación entre issues creadas y la media.
        - Fórmula: (issues_usuario / media_issues) * 10.

    3. Pull requests (20%):
        - Se otorga una nota proporcional al número de pull requests cerrados y mergeados.
        - Máximo: 10.

    4. Workflows (20%):
        - Si un usuario modifica un archivo de workflow, obtiene una nota fija de 10.

    5. Tests (20%):
        - Nota según los tipos de tests realizados:
            - 10: Todos los tipos.
            - 5: Tres tipos.
            - 2: Dos tipos.
            - 1: Un tipo.
            - 0: Ningún tipo.

## Notas Adicionales

- Requisitos previos:

    - Secreto GITHUB_TOKEN configurado en el repositorio.
    - Archivos de test identificables en los commits.

- Resultados:

    - El archivo markdown se encuentra en la carpeta docs del repositorio.
    - Puede ser revisado y actualizado manualmente.
