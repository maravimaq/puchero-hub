# PUCHERO-HUB

* Grupo 2  
* Curso escolar: 2024/2025  
* Asignatura: Evolución y Gestión de la Configuración

# Miembros <!--{#miembros}-->

| Miembro | Implicación |
| :---- | :---- |
| Ávila Maqueda, María del Mar | 10 |
| Blanco Mora, David  | No procede |
| del Junco Obregón, Juan | 10 |
| González Marcos, Pedro | No procede |
| Mejías Buitrago, Pablo | 7.5 |
| Solís Alfonso, Julio | 3 |

## Índice

[Miembros](#miembros)

[Indicadores del Proyecto](#indicadores-del-proyecto)

[Integración con otros equipos](#integración-con-otros-equipos)

[Resumen Ejecutivo (800 palabras)](#resumen-ejecutivo-\(800-palabras\))

[Descripción del sistema (1500 palabras)](#descripción-del-sistema-\(1500-palabras\))

[Visión global del proceso de desarrollo (1500 palabras)](#visión-global-del-proceso-de-desarrollo-\(1500-palabras\))

[Entorno de desarrollo (800 palabras)](#entorno-de-desarrollo-\(800-palabras\))

[Ejercicio de propuesta de cambio](#ejercicio-de-propuesta-de-cambio)

[Conclusiones y trabajo futuro](#conclusiones-y-trabajo-futuro)

# Indicadores del Proyecto <!--{#indicadores-del-proyecto}-->

| Miembro del equipo | Horas | Commits | LoC | Test | Issues | Work Item |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| Ávila Maqueda, María del Mar  | 153 | 117 | 6416 | 70 | 30 | Download All Datasets, Create Communities |
| Blanco Mora, David  | No procede | No procede | No procede | No procede | No procede | No procede |
| del Junco Obregón, Juan | 148 | 117 | 5856 | 88 | 24 | Fakenodo, New Test Cases |
| González Marcos, Pedro | No procede | No procede | No procede | No procede | No procede | No procede |
| Mejías Buitrago, Pablo | 96 | 80 | 2515 | 18 | 17 | View User Profile  |
| Solís Alfonso, Julio | 62 | 13 | 1390 | 16 | 6 | Advanced Filtering |
| **TOTAL** | 459 | 327 | 16177 | 192 | 77 | 6 |

* **Advanced Filtering**: Como usuario quiero filtrar por número de características, números de productos, etc. para obtener datasets de acuerdo a mis necesidades.
* **New Test Cases**: Crear nuevos tests unitarios, de interfaz, de carga y de integración en los distintos modulos que componen el proyecto para aumentar la cobertura total
* **View User Profile**: Como usuario, quiero poder hacer click en el perfil de un usuario para ver sus datasets subidos.
* **Download all Datasets**: Como usuario quiero que al acceder a la página de uvlhub se me permita descargar todos los datasets existentes en la página. Además quiero que estén disponibles en formato pdf, json, cnf, splx y uvl. 
* **Create communities**: Como usuario quiero poder crear una comunidad, editar y/o eliminar las comunidades que he creado yo y unirme a comunidades creadas por otros usuarios. Además al subir un dataset quiero poder elegir si asociar o no un dataset a una comunidad, y en caso de que la asocie quiero que los usuarios de esa comunidad puedan verlos.   

# Integración con otros equipos <!--{#integración-con-otros-equipos}-->

No procede.

# Resumen Ejecutivo *(800 palabras)* <!--{#resumen-ejecutivo-(800-palabras)}-->

El proyecto se centra en el desarrollo y mejora de uvlhub.io, una plataforma para la gestión y exploración de datasets. Su objetivo es optimizar la experiencia del usuario, fomentar la colaboración entre sus miembros y garantizar la calidad del software. A lo largo del trabajo se han implementado diversas funcionalidades clave.

Entre las funcionalidades implementadas destaca el **sistema de filtrado avanzado**, diseñado para realizar búsquedas precisas de datasets en función de atributos específicos como el número de características o productos. Esto permite a los usuarios localizar datos relevantes de forma más rápida y eficiente, optimizando la experiencia general en la plataforma.

Otra mejora importante ha sido el desarrollo de **nuevos casos de prueba**, enfocados en cuatro áreas principales: pruebas unitarias, de interfaz, de carga y de integración. Estas pruebas han aumentado significativamente la cobertura de código, garantizando la robustez y fiabilidad del sistema.

Se añadió, también, la funcionalidad de **visualización de perfiles de usuario**, permitiendo que los usuarios puedan consultar los datasets subidos por otros miembros de la plataforma. Esto fomenta la transparencia y el intercambio de conocimientos dentro de la comunidad, haciendo que la plataforma sea un entorno más interactivo y colaborativo.

Además, se ha trabajado en la **descarga masiva de datasets**, una funcionalidad que permite a los usuarios descargar todos los datasets disponibles en un solo clic y en múltiples formatos, como PDF, JSON, CNF, SPLX y UVL. Esta capacidad asegura la compatibilidad de los datos con diversas herramientas externas, simplificando el acceso y la reutilización de la información según las necesidades del usuario.

También se ha implementado un **sistema de comunidades** que permite a los usuarios crear, editar, eliminar y unirse a comunidades existentes. Estas comunidades sirven como espacios colaborativos donde los usuarios pueden compartir datasets relacionados con intereses comunes. Además, al subir un dataset, es posible asociarlo a una comunidad específica, haciendo que esté disponible para los miembros de dicha comunidad. Esta funcionalidad refuerza la interacción social y la colaboración dentro de la plataforma.

El desarrollo de estas funcionalidades presentó diversos retos, como la integración de nuevas capacidades sin comprometer el rendimiento del sistema existente. También se enfrentaron desafíos relacionados con la coordinación del equipo y el diseño de pruebas para módulos complejos. Estos obstáculos se superaron gracias a una planificación adecuada, revisiones constantes de código y el uso de herramientas de gestión como **Zenhub** que garantizaron un flujo de trabajo eficiente.

El impacto de estas mejoras ha sido significativo. La plataforma ha evolucionado hacia una herramienta más accesible, colaborativa y robusta. Los usuarios ahora cuentan con herramientas más avanzadas para buscar, descargar y gestionar datasets, mientras que las comunidades y los perfiles fomentan un entorno interactivo y orientado al intercambio de conocimiento. Además, la mayor cobertura de pruebas garantiza un software más fiabley mejora la experiencia general.

En resumen, este trabajo ha permitido transformar uvlhub.io en una plataforma más eficiente, accesible y colaborativa, adaptada a las necesidades de sus usuarios. Las mejoras implementadas aseguran una experiencia optimizada en la búsqueda, gestión y descarga de datasets, al tiempo que fomentan la interacción social y la calidad del software.

## Descripción del sistema *(1500 palabras)* <!--{#descripción-del-sistema-(1500-palabras)}-->

### Descripción del Sistema Desarrollado

El sistema desarrollado representa una plataforma robusta y escalable diseñada para la gestión, exploración y colaboración en torno a datasets. Desde un punto de vista funcional y arquitectónico, el sistema implementa características avanzadas como filtrado dinámico, gestión de perfiles de usuario, comunidades, y workflows automatizados. Todo esto está construido utilizando una arquitectura basada en el patrón **Modelo-Vista-Controlador (MVC)**, complementada con pipelines de CI/CD para garantizar la calidad y la eficiencia.

---

### Visión Funcional

Desde el punto de vista funcional, el sistema aborda tres áreas clave:

1. **Exploración de Datasets**:

   - Los usuarios pueden buscar y filtrar datasets según criterios como título, autor, rango de fechas, tamaño, tipo de publicación y etiquetas.

   - Resultados ordenados por fecha de creación (ascendente o descendente).

   - Interfaz intuitiva que permite búsquedas rápidas y precisas.

2. **Gestión de Comunidades**:

   - Permite a los usuarios crear, editar y eliminar comunidades.

   - Los usuarios pueden asociar datasets a comunidades, fomentando la colaboración y el intercambio de información.

   - Visualización de comunidades no unidas, con la posibilidad de unirse a ellas. Y en otra página de comunidades unidas.

3. **Descarga de Datasets**:

   - Funcionalidad para descargar todos los datasets disponibles en un solo clic.

   - Soporte para conversión automática y descarga a múltiples formatos: PDF, JSON, CNF, SPLX y UVL.

   - Aumenta la accesibilidad y facilita la interoperabilidad con herramientas externas.

4. **Gestión de Perfiles de Usuario**:

   - Resumen del perfil propio, que incluye datasets subidos.

   - Visualización de perfiles públicos de otros usuarios y sus datasets compartidos.

5. **Automatización con Workflows**:

   - Análisis de contribuciones de colaboradores en términos de commits, issues cerradas, pull requests y tests.

   - Actualización automática de badges de cobertura de código.

   - Integración con Zenhub para mover automáticamente issues y pull requests entre pipelines.

---

### Visión Arquitectónica

El sistema utiliza una arquitectura basada en **MVC**, que organiza el código en componentes modulares y cohesivos:

1. **Modelo**:
   
   - Representa las estructuras de datos y la lógica de negocio subyacente.
   
   - Ejemplos: `DataSet`, `Community`, `UserProfile`.

2. **Vista**:
   
   - Define la interfaz de usuario mediante plantillas HTML dinámicas y formularios interactivos.
   
   - Ejemplos: páginas para explorar datasets, gestionar comunidades y editar perfiles.

3. **Controlador**:
   
   - Maneja las solicitudes del usuario y coordina entre el modelo y la vista.
   
   - Ejemplos: rutas para explorar datasets (`/explore`), gestionar comunidades (`/community/*`) y editar perfiles (`/profile/edit`).

4. **Pipelines de CI/CD**:
   
   - Automatizan tareas críticas como pruebas, análisis de rendimiento y despliegue de cambios.

---

### Descripción Técnica de los Componentes

#### **1. Explore Module**

Este módulo permite buscar y filtrar datasets mediante un conjunto amplio de criterios.

- **Modelo**:

  - Se utiliza `DataSet` como entidad principal, enriquecida con metadatos de autor, tipo de publicación y etiquetas.

  - Subconsultas en SQL calculan el tamaño total y el número de archivos relacionados con un dataset.

- **Controlador**:

  - Ruta `/explore` gestiona solicitudes GET (búsqueda general) y POST (búsqueda filtrada).

  - Utiliza `ExploreService` y `ExploreRepository` para manejar la lógica de negocio y el acceso a datos.

- **Vista**:

  - Plantillas renderizan los resultados y ofrecen un formulario interactivo para los filtros.

#### **2. Communities Module**

Facilita la creación y gestión de comunidades.

- **Modelo**:

  - `Community` representa la estructura de las comunidades, con relaciones a usuarios (miembros y propietarios) y datasets asociados.

- **Controlador**:

  - Rutas como `/community/create` y `/community/join` permiten a los usuarios gestionar comunidades.

  - `CommunityService` encapsula la lógica de negocio, como validaciones y reglas de pertenencia.

- **Vista**:

  - Páginas HTML para listar comunidades, ver detalles y asociar datasets.

#### **3. Profile Module**

Gestiona los perfiles de usuario y su visualización pública.

- **Modelo**:

  - `UserProfile` almacena información personal, como nombre, biografía y preferencias.

- **Controlador**:

  - Rutas como `/profile/edit` y `/public_profile/<user_id>` gestionan la edición y visualización de perfiles.

  - `UserProfileService` valida y actualiza datos en la base de datos.

- **Vista**:

  - Plantillas para editar perfiles y mostrar el resumen de datasets subidos.

#### **4. Workflows**

Automatizan tareas repetitivas y críticas en el desarrollo y mantenimiento.

- **Contributors Performance Analysis**:

  - Analiza métricas de contribución y genera reportes automáticos.

  - Evalúa el desempeño en términos de commits, issues creadas, pull requests y workflows realizados.

- **Update Coverage Badge**:

  - Ejecuta pruebas con `pytest` y actualiza el badge de cobertura de código en Readme.md.

- **Zenhub Integration**:

  - Automatiza la organización de issues y pull requests en pipelines de Zenhub.

---

### Cambios Implementados

#### **1. Explore**

- **Repositorio**:

  - Método `filter` para manejar criterios como título, autor, fechas, tamaño y tipo de publicación independientemente.

- **Servicio**:

  - Capa intermedia para validar y procesar los filtros.

- **Rutas**:

  - `/explore` para búsquedas dinámicas.

- **Access**

    - Modificación de scripts para gestionar los nuevos criterios.

#### **2. Communities**

- **Modelo**:

  - Estructura de `Community`.

- **Controlador**:

  - Rutas para gestionar la creación, edición, y eliminación de comunidades.

  - Rutas para visualizar comunidades unidas y no unidas.

  - Rutas para unirse a una comunidad.

- **Vista**:

  - Campo nuevo para asociar una comunidad en el formulario para subir datasets.

  - Formulario para crear comunidades.

  - Vista de detalles de comunidades, lista de comunidades propias del usuario, lista de comunidades a las que no se ha unido el usuario

#### **3. Profile**

- **Modelo**:

  - `UserProfile` con datasets subidos por el usuario en cuestion.

- **Controlador**:

  - Mostrar datasets subidos.

- **Vista**:

  - Plantillas para mostrar datasets.

#### **4. Download Datasets**

- **Modelo**:

  - Extensiones para soportar conversión de datasets a múltiples formatos.

- **Controlador**:

  - Ruta `/dataset/download/all` para gestionar descargas masivas y conversión.

- **Vista**:

  - Botón que permite descargar todos los datasets en todos los formatos especificados.

#### **5. Casos de Prueba**

- Se han extendido los casos de prueba para cubrir los módulos nuevos y existentes.

- Pruebas integrales en las siguientes áreas:

  - Pruebas unitarias para validación de datos y lógica de negocio.

  - Pruebas de integración para flujos completos entre subsistemas.

  - Pruebas de interfaz con Selenium para garantizar la usabilidad.
  - Pruebas de carga con Locust para validar el rendimiento.

---

### Relación entre Subsistemas

1. **Integración de Comunidades y Datasets**:

   - Los datasets se pueden asociar directamente a comunidades, fomentando la colaboración en grupos específicos

## Visión global del proceso de desarrollo *(1500 palabras)* <!--{#visión-global-del-proceso-de-desarrollo-(1500-palabras)}-->

El desarrollo del sistema ha seguido un proceso iterativo y estructurado, basado en metodologías ágiles y utilizando herramientas modernas para garantizar la calidad del software y la colaboración efectiva entre los desarrolladores. Este enfoque asegura que cada cambio propuesto se integre de manera segura y eficiente en el sistema.

El proceso general incluye las siguientes etapas:

1. **Propuesta y Planificación del Cambio**:
   
   - Los cambios comienzan como issues en herramientas de gestión como Zenhub.
   
   - Se define el alcance del cambio, las dependencias, y los entregables esperados.

2. **Diseño y Análisis**:
   
   - Se revisa la arquitectura existente para determinar el impacto del cambio.
   
   - Se define un plan técnico que incluye el modelo afectado, las rutas requeridas y los cambios necesarios en las vistas.

3. **Implementación**:
   
   - El cambio se desarrolla siguiendo el patrón Modelo-Vista-Controlador (MVC).
   
   - Los desarrolladores utilizan GitHub para manejar el control de versiones, creando ramas específicas para cada issue.

4. **Pruebas**:
   
   - Se implementan pruebas unitarias, de integración, y de interfaz para validar el cambio.
   
   - Las pruebas se ejecutan de manera automatizada en los workflows de GitHub Actions.

5. **Revisión y Code Review**:
   
   - Los pull requests son revisados por otros miembros del equipo para garantizar la calidad del código.
   
   - Se verifica la cobertura de pruebas y que no haya regresiones.

6. **Despliegue**:
   
   - Una vez aprobado, el cambio se fusiona en la rama principal y se despliega al entorno de producción utilizando pipelines automatizados.

### Herramientas Utilizadas

- **GitHub**: Para la gestión del repositorio, issues, y automatización de workflows.

- **Zenhub**: Para la organización de tareas y seguimiento del progreso.

- **GitHub Actions**: Para ejecutar pruebas automatizadas y actualizar badges de cobertura.

- **Selenium**: Para pruebas de interfaz.

- **Locust**: Para pruebas de carga.

- **Python y Flask**: Para la implementación del backend.

### Ejemplo General: Implementación de un Nuevo Módulo

Cuando se agrega un nuevo módulo al sistema, el proceso sigue pasos similares al abordado en la implementación de la funcionalidad de comunidades. A continuación, se describe de manera generalizada cómo se llevaría a cabo el ciclo completo de desarrollo para un módulo nuevo, como por ejemplo un sistema de "Eventos".

#### 1. Propuesta y Planificación del Cambio

- **Issue en Zenhub**:

  - Crear un issue titulado: "Implementar módulo de eventos".

  - Los criterios de aceptación incluirán funcionalidades clave como la creación, edición y eliminación de eventos.

  - Definir la interacción entre eventos y otros módulos, como usuarios o comunidades.

#### 2. Diseño y Análisis
- **Análisis del impacto**:

  - Identificar las entidades necesarias en el modelo, como `Event`.

  - Determinar las rutas y vistas requeridas.

  - Revisar cómo se relacionará con otros módulos, como comunidades o perfiles.

- **Diseño del sistema**:

  - Crear un nuevo servicio `EventService` para manejar la lógica de negocio.

  - Diseñar consultas y validaciones para las operaciones principales.

#### 3. Implementación

- **Modelo**:

  - Crear un nuevo modelo `Event` con campos como nombre, fecha, descripción y relación con comunidades.

- **Servicio**:

  - Implementar métodos en `EventService` como `create_event`, `edit_event` y `delete_event`.

  - Validar permisos, como asegurar que solo los administradores de una comunidad puedan crear eventos asociados a ella.

- **Controlador**:

  - Crear rutas como `/event/create`, `/event/edit/<event_id>` y `/event/delete/<event_id>`.

- **Vista**:

  - Diseñar plantillas HTML para gestionar eventos, incluyendo formularios y tablas de visualización.

#### 4. Pruebas

- **Pruebas Unitarias**:

  - Validar la creación, edición y eliminación de eventos.

  - Probar las restricciones de permisos.

- **Pruebas de Integración**:

  - Verificar que los eventos se visualizan correctamente en las comunidades asociadas.

- **Pruebas de Interfaz**:

  - Usar Selenium para garantizar que los formularios funcionan adecuadamente.

#### 5. Revisión y Code Review

- Crear un pull request con el nuevo módulo y asignar revisores.

- Revisar código, pruebas y documentación asociada.

#### 6. Despliegue

- Fusionar el pull request en la rama principal.

- Desplegar el cambio mediante pipelines de CI/CD.

- Validar la funcionalidad con pruebas de regresión en el entorno de producción.

---

### Ejemplo Aplicado: Asociación de Datasets a Comunidades

La implementación de la funcionalidad de crear comunidades siguió el proceso descrito anteriormente. Esta funcionalidad permite que los usuarios crear una nueva comunidad y perite que otros usuarios se unan a ella. 

## Entorno de desarrollo *(800 palabras)*  <!--{#entorno-de-desarrollo-(800-palabras)}-->

El desarrollo del sistema se realizó utilizando un entorno que integra diversas herramientas, lenguajes y configuraciones, asegurando la compatibilidad y funcionalidad en distintos escenarios. Este apartado detalla las versiones utilizadas, las herramientas instaladas, y los pasos necesarios para la configuración del entorno de desarrollo.

#### Herramientas y Versiones

1. **Lenguaje de Programación**:

   - **Python**: Versión 3.12.3.

   - **Flask**: Versión 3.0.

2. **Base de Datos**:
   
   - **MariaDB**: Version 15.1 Distrib 10.11.8-MariaDB, for debian-linux-gnu (x86_64) using  EditLine wrapper:

3. **Control de Versiones**:
   
   - **Git**: Versión 2.43.
   
   - **GitHub**: Como repositorio central y para integración continua.

4. **Automatización y Pruebas**:
   
   - **GitHub Actions**: Para CI/CD y automatización de workflows.
   
   - **pytest**: Para pruebas unitarias y de integración (versión 8.2.2).
   
   - **Selenium**: Para pruebas de interfaz, usando Selenium Grid en Docker (versión 4.
   22).
   
   - **Locust**: Para pruebas de carga (versión 2.29.1).
   
   - **Rosemary**: Para pruebas (version 0.1).

5. **Otros Componentes**:
   
   - **Docker**: Versión 27.3.1, para la configuración de entornos reproducibles.

#### Entornos de Desarrollo Utilizados

- **Entorno Local**:
  
  Cada desarrollador configuró un entorno local en su máquina utilizando las herramientas mencionadas anteriormente.

- **Entorno Compartido (Docker)**:
  
  Para garantizar consistencia entre los desarrolladores, se utilizó Docker para configurar contenedores que replicaran el entorno de desarrollo local.

- **Entorno de CI/CD**:
  
  GitHub Actions se usó para integrar pruebas y despliegues automáticos.

#### Configuración del Entorno de Desarrollo

Los pasos para configurar y ejecutar el sistema completo son los siguientes:

##### Instalación del Entorno Local

1. **Instalar Dependencias**:
   
   - Instalar Python 3.12.3 siguiendo las instrucciones de la asignatura.
   
   - Instalar MySQL siguiendo las instrucciones de la asignatura.
   
   - Instalar Docker y Docker Compose desde [docker.com](https://www.docker.com/).

2. **Clonar el Repositorio**:
   
   ```bash
   git clone git@github.com:maravimaq/puchero-hub.git
   cd puchero-hub
   ```

3. **Configurar el Entorno Virtual de Python**:
   
   ```bash
   python -m venv venv
   source venv/bin/activate 
   pip install -r requirements.txt
   ```

4. **Configurar la Base de Datos**:
   
   - Crear la base de datos MySQL:
     
     ```bash
     sudo apt install mariadb-server -y
     sudo systemctl start mariadb
     sudo mysql_secure_installation
          - Enter current password for root (enter for none): (enter)
          - Switch to unix_socket authentication [Y/n]: `y`
          - Change the root password? [Y/n]: `y`
              - New password: `uvlhubdb_root_password`
              - Re-enter new password: `uvlhubdb_root_password`
          - Remove anonymous users? [Y/n]: `y`
          - Disallow root login remotely? [Y/n]: `y` 
          - Remove test database and access to it? [Y/n]: `y`
          - Reload privilege tables now? [Y/n] : `y`
     
     sudo mysql -u root -p
        CREATE DATABASE uvlhubdb;
        CREATE DATABASE uvlhubdb_test;
        CREATE USER 'uvlhubdb_user'@'localhost' IDENTIFIED BY 'uvlhubdb_password';
        GRANT ALL PRIVILEGES ON uvlhubdb.* TO 'uvlhubdb_user'@'localhost';
        GRANT ALL PRIVILEGES ON uvlhubdb_test.* TO 'uvlhubdb_user'@'localhost';
        FLUSH PRIVILEGES;
        EXIT;
     ```
    - Instalar dependencias:
     
     ```bash
      pip install --upgrade pip
      pip install -r requirements.txt

     ```
    
    - Instalar Rosemary:
    
     ```bash
     pip install -e ./
     ```

    - Migrar la base de datos:
     
     ```bash
     flask db upgrade
     ```
    - Popular la base de datos:
     
     ```bash
     rosemary db:seed
     ```

5. **Iniciar el Servidor Local**:
   
   ```bash
   flask run --host=0.0.0.0 --reload --debug
   ```

##### Configuración con Docker

1. **Construir los Contenedores e instalar Drivers de Selenium**:
   
  Antes de nada seguir las instrucciones del documento [Selenium_in_Docker](https://github.com/maravimaq/puchero-hub/blob/main/docs/Selenium_in_Docker.md)

2. **Verificar el Estado**:
   
   - Acceder a la aplicación en `http://localhost`.
   
   - Asegurarse de que los servicios estén activos dentro de los contenedores.
    ```bash
   docker ps
   ```

##### Ejecución de Pruebas

1. **Abrir web_app_container bash**
- Para ejecutar las pruebas con Rosemary CLI, primero debe iniciar la terminal de web_app_container:
  ```bash
  docker exec -it web_app_container bash
  ```

2. **Pruebas Unitarias e Integración del <module_name>**:
   
   ```bash
   rosemary test <module_name>
   ```

3. **Pruebas de Interfaz con Selenium**:
   
    ```bash
    rosemary selenium <module_name>
    ```

3. **Pruebas de Carga con Locust**:
   
   ```bash
   rosemary locust <module_name>
   ```


## Ejercicio de propuesta de cambio <!--{#ejercicio-de-propuesta-de-cambio}-->

### Ejemplo Ilustrativo: Proceso Completo de un Cambio en el Sistema

Este ejercicio detalla cómo se implementó la funcionalidad de creación, edición y eliminación de comunidades en el sistema, utilizando las vistas y pruebas proporcionadas.

---

### **Propuesta y Planificación del Cambio**

#### Escenario:

Se requiere permitir a los usuarios crear, editar y eliminar comunidades dentro del sistema. Cada comunidad debe incluir un nombre, descripción y una lista de miembros, comenzando con el usuario que la crea como propietario.

#### Acciones:

1. Crear un issue en **Zenhub**:
   
   - Título: "Create Communities".
   
   - Criterios de aceptación:
   
     - An identified user is able to create new communities..

2. Definir dependencias y asignar tareas.

---

### **Diseño y Análisis**

#### Impacto en los Componentes:

1. **Modelo**:

   - `Community`: Relacionado con `User` para gestionar propietarios y miembros.

2. **Vistas**:

   - `create.html` para crear comunidades.

   - `index.html` para listar comunidades del usuario.

3. **Controlador**:

   - Rutas para crear, editar y eliminar comunidades.

#### Validaciones Requeridas:

- El nombre de la comunidad debe ser único.

- El usuario autenticado se agrega automáticamente como miembro y propietario.

---

### **Implementación**

#### 1. Cambios en el Modelo:

El modelo `Community` en `models.py` define las comunidades y sus relaciones con los usuarios.

```python
class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    members = db.relationship('User', secondary='community_members', backref='communities')
```

#### 2. Cambios en el Servicio:

El servicio gestiona la lógica de negocio. Ejemplo de creación:

```python
def create_community(name, description, owner):
    if Community.query.filter_by(name=name).first():
        raise ValueError("Community name must be unique")
    community = Community(name=name, description=description, owner_id=owner.id)
    community.members.append(owner)
    db.session.add(community)
    db.session.commit()
    return community
```

#### 3. Cambios en el Controlador:

Se agregaron rutas para crear y listar comunidades:

```python
@app.route('/community/create', methods=['GET', 'POST'])
def create_community():
    form = CommunityForm()
    if form.validate_on_submit():
        try:
            community = create_community(form.name.data, form.description.data, current_user)
            return redirect(url_for('community.show', community_id=community.id))
        except ValueError as e:
            form.name.errors.append(str(e))
    return render_template('create.html', form=form)
```

#### 4. Cambios en las Vistas:

##### `create.html`:

Formulario para la creación de comunidades:

```html
<form method="POST" action="{{ url_for('community.create_community') }}">
    {{ form.hidden_tag() }}
    <div class="form-group mb-3">
        <label for="name" class="form-label">{{ form.name.label }}</label>
        {{ form.name(class="form-control") }}
    </div>
    <div class="form-group mb-3">
        <label for="description" class="form-label">{{ form.description.label }}</label>
        {{ form.description(class="form-control") }}
    </div>
    <button type="submit" class="btn btn-primary">Create Community</button>
</form>
```

##### `index.html`:

Vista de comunidades del usuario:

```html
{% for community in communities %}
<div class="list-group-item">
    <h5><a href="{{ url_for('community.show', community_id=community.id) }}">{{ community.name }}</a></h5>
    <p>{{ community.description }}</p>
</div>
{% endfor %}
```

---

### **Pruebas**

#### Pruebas Unitarias:

Ejemplo de prueba para la creación de comunidades:

```python
def test_create_community_service(test_client):
    with test_client.application.app_context():
        owner = User.query.filter_by(email='owner@example.com').first()
        created_community = service.create(name="Test Community", description="Description", owner=owner)
        assert created_community.name == "Test Community"
```

#### Pruebas de Integración:

Ejemplo para la creación desde la vista:

```python
def test_create_community(test_client):
    login(test_client, "testuser@example.com", "test1234")
    response = test_client.post('/community/create', data={'name': 'New Community', 'description': 'Description'}, follow_redirects=True)
    assert response.status_code == 200
```

#### Pruebas de Interfaz:

Verificar el botón para crear nuevas comunidades:

```python
def test_create_new_community_button():
    driver.find_element(By.LINK_TEXT, "Create New Community").click()
    assert "create" in driver.current_url
```

#### Pruebas de Carga:

Simulación de carga con Locust:

```python
@task(2)
def create_community(self):
    new_community = {"name": "Load Test Community", "description": "Description"}
    self.client.post("/community/create", data=new_community)
```

---

### **Revisión y Code Review**

1. Crear un pull request en GitHub con los cambios realizados.

2. Revisar pruebas y documentación adjunta.

3. Validar mediante los workflows en GitHub Actions.

---

### **Despliegue**

1. Fusionar el pull request en la rama principal.

2. Ejecutar el pipeline de CI/CD para pruebas y despliegue.

3. Verificar en producción:
   - La correcta creación y visualización de comunidades.
   - La edición y eliminación solo por propietarios.

---

Este ejercicio ilustra cómo implementar una funcionalidad desde su planificación hasta su despliegue, asegurando la calidad mediante pruebas exhaustivas.


## Conclusiones y trabajo futuro <!--{#conclusiones-y-trabajo-futuro}-->

En definitiva, el desarrollo del proyecto ha sido complicado, y durante este, nos hemos enfrentado a muchos retos y a muchas complicaciones, que nos han impedido realizar el trabajo sin conflictos ni fallos. A pesar de ello, nos podemos sentir satisfechos con nuestro desempeño general, ya que a pesar de las circunstancias, de las marchas y abandonos de compañeros, hemos sido capaces de hacer frente a las adversidades, y sacar un proyecto completo que cumpla con los requisitos mínimos exigidos por la asignatura.

Como mejora y crítica para el curso siguiente, nosotros recomendaríamos revisar la implementación de tests de interfaz con `Selenium`, y enseñar a los alumnos como funciona esta interfaz para hacer test, ya que sin ninguna duda, ha sido el mayor problema general para todos los grupos. Por ejemplo, lo realizado por nuestro grupo para enlazar `Docker con Selenium`, al final nos ha ayudado a tener un sistema de ejecución de pruebas más intuitivo, y consideramos que podría estar bien para enseñar a los alumnos del siguiente año, cómo funciona `Selenium`, y asegurarse un correcto funcionamiento de la interfaz. Nuestro documento que recopila toda la información de la interfaz `Selenium` en `Docker` es el siguiente: [Selenium_in_Docker](https://github.com/maravimaq/puchero-hub/blob/main/docs/Selenium_in_Docker.md).

Además, otra crítica que tenemos es *el verdadero valor del proyecto en la nota de la asignatura*, ya que da igual lo que se haga en el proyecto, lo que se trabaje, y el tiempo que se eche en este, que si se saca menos de un 4 en los `exámenes práctico y teórico`, el alumno tendriá que ir a la `convocatoria de julio`, y todo lo hecho en el proyecto perdería todo su valor. Decimos que pierde su valor, porque en julio no habría parte correspondiente al proyecto, sino solo parte teórica y práctica, y para la mayoria de alumnos, el hecho de sacar menos de un 4 en la parte individual, podrían echar a perder un 80 o 90% de la nota dependiendo de su itinerario escogido. Por ello, consideramos que el proyecto debería tener más valor ya que requiere de mucha dedicación y tiempo, o incluso, si no se le da más valor, restarle prioridad e importancia a otras partes, como por ejemplo, bajando la nota mínima de las `partes práctica y teórica`, y así poder facilitar al alumnado, el que emplee un mayor esfuerzo y tiempo en el proyecto.