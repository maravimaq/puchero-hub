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
| Mejías Buitrago, Pablo | 6 |
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
| Ávila Maqueda, María del Mar  | 153 | 113 | 5662 | 70 | 30 | Download All Datasets, Create Communities |
| Blanco Mora, David  | No procede | No procede | No procede | No procede | No procede | No procede |
| del Junco Obregón, Juan | 148 | 116 | 5209 | 88 | 22 | Fakenodo, New Test Cases |
| González Marcos, Pedro | No procede | No procede | No procede | No procede | No procede | No procede |
| Mejías Buitrago, Pablo | 96 | 69 | 1873 | 18 | 11 | View User Profile  |
| Solís Alfonso, Julio | 52 | 4 | 691 | 15 | 2 | Advanced Filtering |
| **TOTAL** | 449 | 302 | 13435 | 191 | 65 | 6 |

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

  - Evalúa el desempeño en términos de commits, issues cerradas, pull requests y tests realizados.

- **Update Coverage Badge**:

  - Ejecuta pruebas con `pytest` y actualiza el badge de cobertura de código.

- **Zenhub Integration**:

  - Automatiza la organización de issues y pull requests en pipelines de Zenhub.

---

### Cambios Implementados

#### **1. Explore**

- **Repositorio**:

  - Método `filter` para manejar criterios como título, autor, fechas, tamaño y tipo de publicación.

- **Servicio**:

  - Capa intermedia para validar y procesar los filtros.

- **Rutas**:

  - `/explore` para búsquedas dinámicas.

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

*Debe dar una visión general del proceso que ha seguido enlazándolo con las herramientas que ha utilizado. Ponga un ejemplo de un cambio que se proponga al sistema y cómo abordaría todo el ciclo hasta tener ese cambio en producción. Los detalles de cómo hacer el cambio vendrán en el apartado correspondiente.*

## Entorno de desarrollo *(800 palabras)*  <!--{#entorno-de-desarrollo-(800-palabras)}-->

*Debe explicar cuál es el entorno de desarrollo que ha usado, cuáles son las versiones usadas y qué pasos hay que seguir para instalar tanto su sistema como los subsistemas relacionados para hacer funcionar el sistema al completo. Si se han usado distintos entornos de desarrollo por parte de distintos miembros del grupo, también debe referenciarlo aquí.*

## Ejercicio de propuesta de cambio <!--{#ejercicio-de-propuesta-de-cambio}-->

*Se presentará un ejercicio con una propuesta concreta de cambio en la que a partir de un cambio que se requiera, se expliquen paso por paso (incluyendo comandos y uso de herramientas) lo que hay que hacer para realizar dicho cambio. Debe ser un ejercicio ilustrativo de todo el proceso de evolución y gestión de la configuración del proyecto.*

## Conclusiones y trabajo futuro <!--{#conclusiones-y-trabajo-futuro}-->

*Se enunciarán algunas conclusiones y se presentará un apartado sobre las mejoras que se proponen para el futuro (curso siguiente) y que no han sido desarrolladas en el sistema que se entrega*