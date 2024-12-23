### <p style="text-align: center;">Universidad de Sevilla</p> 

#### <p style="text-align: center;">Escuela Técnica Superior de Ingeniería Informática</p>  

# <p style="text-align: center;">Acta fundacional</p>

### <p style="text-align: center;">Puchero-hub</p>

<p style="text-align: center;">
  <img src="static/logo_puchero_hub.png" alt="Logo de Puchero-hub" style="width: 300px;">
</p>

#### <p style="text-align: center;">Grado en Ingeniería Informática - Ingeniería del Software</p>
#### <p style="text-align: center;">Evolución y Gestión de la Configuración</p>

##### <p style="text-align: center;">Curso 2024-2025</p>

# Índice
1. [Miembros de puchero-hub](#id1)
2. [¿Qué es puchero-hub?](#id2)
3. [Roles del equipo](#id3)
4. [Repositorio en GitHub](#id4)
- [i. Estructura del repositorio](#id41)
5. [Políticas](#id5)
- [i. Política de Commits ](#id51)
- [ii. Política de Ramas ](#id52)
- [iii.Política de Issues ](#id53)
- [iv. Política de Versionado ](#id54)
6. [Integración Continua](#id6)
7. [Despliegue Continuo](#id7)
8. [Gestión de Conflictos](#id8)
9. [Gestión de Incidencias](#id9)


<div id='id1'></div>


# 1. Miembros de puchero-hub
<div style="text-align: center;">
  <table style="margin: auto; border-collapse: collapse; width: 60%;">
    <thead>
      <tr style="background-color: #f2f2f2; text-align: center;">
        <th style="padding: 8px; border: 1px solid #ddd;"><strong>Apellidos, Nombre</strong></th>
        <th style="padding: 8px; border: 1px solid #ddd;"><strong>uvus</strong></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="text-align: left; padding: 8px; border: 1px solid #ddd;">Ávila Maqueda, María del Mar</td>
        <td style="text-align: left; padding: 8px; border: 1px solid #ddd;">maravimaq</td>
      </tr>
      <tr>
        <td style="text-align: left; padding: 8px; border: 1px solid #ddd;">Blanco Mora, David</td>
        <td style="text-align: left; padding: 8px; border: 1px solid #ddd;">davblamor</td>
      </tr>
      <tr>
        <td style="text-align: left; padding: 8px; border: 1px solid #ddd;">del Junco Obregón, Juan</td>
        <td style="text-align: left; padding: 8px; border: 1px solid #ddd;">juanjunobr</td>
      </tr>
      <tr>
        <td style="text-align: left; padding: 8px; border: 1px solid #ddd;">Mejías Buitrago, Pablo</td>
        <td style="text-align: left; padding: 8px; border: 1px solid #ddd;">pabmejbui</td>
      </tr>
      <tr>
        <td style="text-align: left; padding: 8px; border: 1px solid #ddd;">Solís Alfonso, Julio</td>
        <td style="text-align: left; padding: 8px; border: 1px solid #ddd;">julsolalf</td>
      </tr>
    </tbody>
  </table>
</div>


<div id='id2'></div>


# 2. ¿Qué es Puchero-hub?
**Puchero-hub** es un un proyecto creado con el fin de implementar nuevas funcionalidades a la aplicación web uvlhub.io. **Uvlhub** es un repositorio, desarrollado por Diverso-Lab, que consiste una serie de modelos de características siguendo el formato UVL y está integrado con Flamapy y Zenodo.

El proyecto tiene como requisitos principales el cumpliemento de una serie de milestones o entregables, en los que se deberá entregar, el proyecto, siendo este funcional y con diversas adiciones extras. Estas milestones están representadas en la página web de la asignatura *Evolución y Gestión de la Configuración*, [Wiki - EGC](https://1984.lsi.us.es/wiki-egc/index.php/P%C3%A1gina_Principal) , en la sección con nombre: *Proyecto - 24/25*.

- **M0**: Inscripción de los equipos (+info)  
  *Viernes, 4 de Octubre*

- **M1**: Sistema funcionando y pruebas (+info)  
  *Miércoles, 23 de Octubre*

- **M2**: Sistema funcionando y con incrementos (+info)  
  *Miércoles, 13 de Noviembre*

- **M3**: Entrega de proyectos y defensas (+info)  
  *Miércoles, 18 de Diciembre*


<div id='id3'></div>


# 3. Roles del equipo
El equipo está formado por los miembros mencionados anteriormente, pero aparte de estos miembros, el desarrollo del proyecto tiene una estructura de organización a tener en cuenta. Dicha estructura está repartida en dos roles y/o escalones, *Director del proyecto* y *Equipo de desarrollo*:

- **Equipo de desarrollo**:
  - Ávila Maqueda, María del Mar. *Contacto*: maravimaq@alum.us.es
  - Blanco Mora, David. *Contacto*: davblamor@alum.us.es
  - del Junco Obregón, Juan. *Contacto*: juajunobr@alum.us.es
  - Mejías Buitrago, Pablo. *Contacto*: pabmejbui@alum.us.es
  - Solís Alfonso, Julio. *Contacto*: julsolalf@alum.us.es

- **Director del proyecto**:
  - Romero Organvídez, David. *Contacto*: drorganvidez@us.es


<div id='id4'></div>


# 4. Repositorio en GitHub
Nuestro proyecto se ha realizado subiendo dicho proyecto a un repositorio común en la plataforma GitHub. Este repositorio es el siguiente: [Puchero-hub](https://github.com/maravimaq/puchero-hub.git).

## i. Estructura del repositorio
La estructura principal del proyecto consta de las siguientes carpetas y archivos. Dentro de las carpetas hay más información detallada, pero en este caso hemos decidido mostrar principalmente la estructura del proyecto en general, sin entrar mucho en detalles, nada más para explicar en que consiste cada archivos y carpeta:

<div id='id41'></div>

- **.env.docker.example**  
  ➡ Ejemplo de configuración de entorno para entornos Docker.
- **.env.docker.production.example**  
  ➡ Ejemplo de configuración de entorno para producción en Docker.
- **.env.local.example**  
  ➡ Ejemplo de configuración de entorno para desarrollo local.
- **.env.vagrant.example**  
  ➡ Ejemplo de configuración de entorno para configuraciones con Vagrant.
- **.flake8**  
  ➡ Configuración para la herramienta de estilo de código Python Flake8.
- **.gitattributes**  
  ➡ Configuración para el tratamiento de archivos en Git.
- **.gitignore**  
  ➡ Lista de archivos y carpetas que Git debe ignorar.
- **.moduleignore**  
  ➡ Archivos y carpetas que deben excluirse al empaquetar el módulo.
- **README.md**  
  ➡ Documentación principal del proyecto con información sobre instalación y uso.
- **coverage.svg**  
  ➡ Indicador visual del porcentaje de cobertura de pruebas.
- **requirements.txt**  
  ➡ Lista de dependencias necesarias para el proyecto.
- **setup.py**  
  ➡ Configuración del paquete para su instalación o distribución.
- **github/workflows/**  
  ➡ Configuraciones de automatización para CI/CD mediante GitHub Actions.
- **app/**  
  ➡ Contiene el código principal de la aplicación, incluyendo vistas, modelos, rutas y servicios.  
  - **modules/**  
    ➡ Módulos organizados por funcionalidades específicas, como autenticación, comunidad, etc.  
  - **static/**  
    ➡ Archivos estáticos como CSS, JavaScript e imágenes.  
    - **css/** ➡ Estilos CSS de la aplicación.  
    - **js/** ➡ Scripts JavaScript para funcionalidades interactivas.  
    - **images/** ➡ Imágenes como logos y otros recursos visuales.  
  - **templates/**  
    ➡ Plantillas HTML para las vistas.  
    - **base.html** ➡ Plantilla base compartida.  
    - **layout.html** ➡ Estructura general de las páginas.  
- **core/**  
  ➡ Configuraciones esenciales y componentes principales del proyecto, como extensiones y configuraciones base.
- **docker/**  
  ➡ Archivos relacionados con configuraciones y scripts para Docker, facilitando la creación de contenedores.
- **docs/**  
  ➡ Documentación adicional del proyecto, como especificaciones técnicas y manuales de referencia.
- **migrations/**  
  ➡ Archivos generados por herramientas de migración para la gestión del esquema de la base de datos.
- **rosemary/**  
  ➡ Módulos específicos para funcionalidades adicionales o integraciones personalizadas.
- **scripts/**  
  ➡ Scripts de utilidad para tareas de mantenimiento, despliegue o configuración.
- **vagrant/**  
  ➡ Archivos de configuración para entornos de desarrollo usando Vagrant.


<div id='id5'></div>


# 5. Políticas
En esta sección vamos a hablar de las distintas políticas a seguir por el equipo. Estas políticas son políticas decididas por el conjunto del equipo, y deben ser acatadas por todos los miembros de este.

<div id='id51'></div>

## i. Política de Commits
Nuestro equipo sigue una política de commits que se llama **Conventional Commits**. # Política de Commits: Conventional Commits

La política **Conventional Commits** es un estándar ampliamente utilizado para redactar mensajes de commits de manera clara y estructurada. Su objetivo principal es mantener un historial consistente y fácil de entender, facilitando el trabajo en equipo, la revisión de cambios y el uso de herramientas automatizadas como generación de changelogs y versionado semántico.

### **Estructura del Mensaje de Commit**

Cada mensaje de commit debe seguir la siguiente estructura:

```plaintext
<tipo>(<alcance opcional>): <descripción breve>
```

- **`tipo`**: Describe el propósito del cambio. Por ejemplo: `feat`, `fix`, `docs`, etc.
- **`alcance` (opcional)**: Especifica el módulo, componente o área afectada del proyecto. Por ejemplo: `(login)`, `(API)`.
- **`descripción breve`**: Explica de manera concisa qué se ha hecho.

### Tipos de Commits

A continuación, se describen los principales tipos de commits que seguimos en este proyecto:

#### `feat`: Funcionalidades nuevas
- **Uso**: Commits que añaden nuevas funcionalidades o crean nuevos archivos.
- **Ejemplo**:  

```plaintext
feat(login): añadir autenticación de usuarios
```

#### `fix`: Correcciones de errores
- **Uso**: Commits que corrigen fallos o errores en el código.
- **Ejemplo**: 

```plaintext
fix(api): corregir error de validación en el endpoint de usuarios
```

#### `docs`: Documentación
- **Uso**: Commits relacionados con cambios en la documentación, como manuales o README.
- **Ejemplo**:  

```plaintext
docs(readme): actualizar requisitos de instalación
```

#### `test`: Pruebas
- **Uso**: Commits que contienen cambios o adiciones en las pruebas, como unitarias o de integración.
- **Ejemplo**:  

```plaintext
test(auth): añadir pruebas para la autenticación de usuarios
```

### Ventajas de Usar Conventional Commits

- **Consistencia**: Los mensajes son uniformes, lo que facilita la lectura del historial de commits.
- **Automatización**: Se pueden generar changelogs automáticos y realizar versionado semántico.
- **Colaboración**: Facilita la comunicación dentro del equipo sobre los cambios realizados.

Esta política asegura que cada commit refleje de manera precisa el trabajo realizado y permite un mejor mantenimiento del proyecto a lo largo del tiempo.

<div id='id52'></div>

## ii. Política de Ramas
En nuestro proyecto seguimos el flujo de trabajo **Feature Branch Workflow**, el cual permite un desarrollo organizado y colaborativo. A continuación, se detalla el proceso que seguimos para gestionar las ramas:

### **1. Creación de ramas independientes**
- Para cada nueva funcionalidad o corrección, se crea una rama independiente basada en la rama principal (`main`).
- Las ramas se nombran de manera descriptiva para identificar claramente su propósito, siguiendo estas convenciones:
  - **`feature/<descripción>`**: Para nuevas funcionalidades.
  - **`fix/<descripción>`**: Para correcciones de errores.
  - **`hotfix/<descripción>`**: Para correcciones críticas en producción.
  - **`docs/<descripcion>`**: Para documentos.

**Ejemplos de nombres de ramas:**
- `feature/autenticacion_usuario`
- `feature/soporte_multilenguaje`
- `fix/correccion_login`
- `hotfix/error_critico_pago`
- `docs/policy_documents`

### **2. Desarrollo en las ramas independientes**
- Todo el desarrollo relacionado con la funcionalidad o corrección específica se realiza dentro de la rama creada.
- Esto asegura que la rama principal (`main`) permanezca siempre estable y lista para su uso.

### **3. Creación de una Pull Request**
- Una vez completado el desarrollo en la rama independiente, se crea una **Pull Request (PR)** hacia la rama principal (`main`).
- En la PR, se describen los cambios realizados y se incluye cualquier información relevante.

### **4. Revisión por parte del equipo**
- Nosotros hemos implementado que no haga falta revisión por parte del equipo, ya que eso consideramos que provoca retrasos a la hora de realizar el proyecto.
- Como único requisito de revision tenemos que no se suba nada que de error, o fallo. Todo lo que se suba al repositorio debe ser funcional.

### **5. Fusión con la rama principal**
- La Pull Request será **mergeada** con la rama `main`.

### **6. Eliminación de la rama**
- Después de la fusión, la rama de funcionalidad puede ser **eliminada** para mantener el repositorio limpio y organizado.
- No tenemos la obligación impuesta de eliminar o no la rama. Hay libertad en este aspecto.

### **Ventajas de esta política**
- **Colaboración efectiva**: La revisión por parte de otros desarrolladores mejora la calidad del código.
- **Estructura clara**: Las ramas independientes organizan el trabajo y protegen la estabilidad de `main`.
- **Control de calidad**: Solo los cambios revisados y aprobados llegan a `main`.

Con esta política, aseguramos un flujo de trabajo eficiente, colaborativo y de alta calidad en el desarrollo de nuestro proyecto.


<div id='id53'></div>


## iii.Política de Issues
Nuestro equipo ha decidido no seguir una política de Issues específica en cuanto al nombramiento de estas. Básicamente, los nombres de estas van a seguir un formato de explicación descriptiva de la Issue, y en inglés.

A cada Issue se le asignará una etiqueta según sobre el tipo de issue que sea. Para ello vamos a usar las etiquetas dadas por defecto en github, junto a la adición de una nueva, que recibe el nombre `test`. Esta última no se encuentra en github, y la vamos a usar para las issues dedicadas a las pruebas.

Además, para el uso y empleo detallado de las issues, hemos usado la extensión y plataforma Zenhub, la cuál mediante un tablero nos permite conectar las issues a las pull requests, y que en este tablero, se desplacen automáticamente al estar conectadas, y tras realizar una pull request sobre esa issue.

Por último, se ha tomado la decisión de que las Issues se agruparán en Épicas para así mantener una organización más específica y detallada.


<div id='id54'></div>


## iv. Política de Versionado
Nuestra política de versionado sigue el esquema **X.Y.Z**, el cual permite identificar de manera clara y estructurada los cambios realizados en el proyecto. Este sistema de versionado facilita el seguimiento de actualizaciones y asegura que todos los miembros del equipo comprendan el impacto de cada cambio en el proyecto.

### **1. Componente X (Versión Mayor)**
- Representa cambios **grandes o disruptivos** que pueden hacer que versiones anteriores queden desfasadas o incompatibles.
- Se utiliza para:
  - Modificaciones significativas en la estructura del proyecto.
  - Cambios que impacten la base del sistema o introduzcan una nueva arquitectura.
  - Lanzamientos que no sean compatibles hacia atrás con versiones anteriores.

**Ejemplo:**
- De `1.5.2` a `2.0.0`: Se introduce una reestructuración completa del sistema.

### **2. Componente Y (Versión Menor)**
- Representa **adiciones de nuevas funcionalidades** que no alteran la estructura general del proyecto ni rompen compatibilidad con versiones anteriores.
- Se utiliza para:
  - Incorporar nuevas características.
  - Mejoras significativas en el sistema que no impactan la base existente.

**Ejemplo:**
- De `1.5.2` a `1.6.0`: Se añade soporte para multilenguaje.

### **3. Componente Z (Correcciones o Cambios Menores)**
- Representa **pequeños ajustes, correcciones o mejoras** que no tienen un impacto significativo en el proyecto.
- Se utiliza para:
  - Correcciones de errores o bugs.
  - Mejoras menores en el rendimiento.
  - Cambios triviales en la documentación o pruebas.

**Ejemplo:**
- De `1.5.2` a `1.5.3`: Se corrige un error en la validación del formulario de login.

### **Ventajas de esta Política**
1. **Claridad**: Permite entender el alcance de los cambios realizados con solo observar el número de versión.
2. **Compatibilidad**: Facilita la planificación para asegurar compatibilidad entre versiones.
3. **Colaboración**: Ayuda al equipo a priorizar cambios según su impacto en el proyecto.

Con esta política de versionado, aseguramos un control preciso y estructurado de las actualizaciones del proyecto, mejorando la comunicación dentro del equipo y con los usuarios.


<div id='id6'></div>


# 6. Integración continua
En nuestro proyecto implementamos **Integración Continua (CI)** utilizando **GitHub Actions**. Esto nos permite mantener un flujo de trabajo eficiente, automatizado y con altos estándares de calidad.

## **Codacy**
Utilizamos **Codacy** como herramienta de análisis estático de código, que nos ayuda a garantizar la calidad y consistencia del código mediante:
- **Revisión automática**: Detecta malas prácticas, problemas comunes y complejidad en el código.
- **Cobertura de código**: Evalúa qué porcentaje del código está cubierto por pruebas.
- **Integración con GitHub**: Proporciona comentarios automáticos en pull requests, facilitando la colaboración del equipo.

Codacy se configura directamente con el repositorio, evaluando cada cambio que se realiza en el proyecto.

## **Update Coverage Badge**
Hemos implementado un workflow llamado **Update Coverage Badge**, diseñado para mantener actualizado el badge de cobertura del código. Este workflow realiza las siguientes tareas:

1. **Ejecuta pruebas**: Corre las pruebas unitarias y de integración para verificar el estado del proyecto.
2. **Genera un badge de cobertura**: Muestra visualmente el porcentaje de código cubierto por pruebas.
3. **Actualiza el badge automáticamente**: Sube el badge actualizado al repositorio, resolviendo conflictos si los hay.

Se ejecuta cada vez que:
- Se realiza un `push` a la rama `main`.
- Se abre o actualiza una pull request hacia `main`.

## **Beneficios de la Integración Continua**
1. **Calidad del código**: Garantiza estándares altos gracias al análisis automático de Codacy.
2. **Automatización**: Reduce tareas manuales con workflows que ejecutan pruebas y actualizan métricas.
3. **Colaboración efectiva**: Los análisis y comentarios automáticos facilitan la revisión del código.
4. **Visibilidad**: El badge de cobertura y las métricas de Codacy proporcionan información clara y actualizada.

Con esta configuración, aseguramos un desarrollo ágil y de calidad, optimizando el flujo de trabajo del equipo.


<div id='id7'></div>


# 7. Despliegue continuo
En nuestro proyecto, hemos implementado un sistema de **Despliegue Continuo (CD)** utilizando **GitHub Actions** y la plataforma **Render**. Este enfoque asegura que cada cambio aprobado en la rama principal (`main`) sea desplegado automáticamente en el entorno de producción, manteniendo un flujo de trabajo ágil y eficiente.

## **Despliegue en Render**
El despliegue automático se activa cada vez que se realiza un `push` a la rama `main`. El workflow de GitHub Actions realiza las siguientes tareas:

1. **Ejecución de Pruebas de Integración**: Antes de proceder al despliegue, todas las pruebas deben pasar correctamente. Esto asegura que solo código funcional se despliegue en producción.
2. **Automatización del Despliegue**: Una vez superadas las pruebas, el workflow despliega automáticamente la aplicación en la plataforma **Render**, actualizando la instancia en producción.

Este proceso garantiza un despliegue confiable y rápido, eliminando la necesidad de realizar operaciones manuales.

## **Zenhub Workflow**
Adicionalmente, utilizamos un workflow personalizado llamado **Zenhub Workflow** para gestionar automáticamente las tareas relacionadas con los issues y pull requests en **Zenhub**, nuestra herramienta de gestión de proyectos.

## **¿Qué hace el Zenhub Workflow?**
1. **Detección de eventos**: El workflow se activa cuando se abren, editan o cierran issues, así como cuando se abren o cierran pull requests.
2. **Actualización automática de pipelines**:
   - Los issues y pull requests se mueven automáticamente entre los pipelines de **Zenhub**, según el evento que ocurra:
     - **New Issues**: Cuando se abre un nuevo issue.
     - **In Progress**: Cuando se abre un pull request.
     - **Review/QA**: Cuando se cierra un pull request.
     - **Done**: Cuando se cierra un issue.
3. **Interacción con la API de Zenhub**:
   - Utiliza la API de Zenhub para mover issues o pull requests al pipeline correspondiente, asegurando una gestión fluida y automatizada del flujo de trabajo.

## **Beneficios del Despliegue Continuo**
1. **Automatización Total**:
   - Todo el proceso, desde la validación hasta el despliegue y la gestión de tareas, está completamente automatizado.
   
2. **Calidad Garantizada**:
   - La ejecución de pruebas asegura que solo código funcional llega a producción.
   
3. **Gestión Eficiente**:
   - El workflow de Zenhub sincroniza automáticamente el estado de las tareas, reduciendo la carga manual del equipo.
   
4. **Despliegue Rápido**:
   - Los cambios llegan a producción en minutos, permitiendo iteraciones ágiles y una respuesta rápida a las necesidades del proyecto.

Con estos workflows, hemos optimizado tanto el despliegue de nuestra aplicación como la gestión del flujo de trabajo del equipo, asegurando un desarrollo ágil y eficiente.


<div id='id8'></div>


# 8. Gestión de Conflictos
En nuestro equipo, reconocemos que los conflictos pueden surgir durante el desarrollo del proyecto. Para mantener un entorno de trabajo colaborativo y eficiente, hemos establecido procedimientos claros para gestionar y resolver estos conflictos de manera justa y constructiva.

## **Conflicto: Inactividad de algún miembro del equipo**
### **Solución:**
1. Los miembros del equipo se pondrán en contacto con la persona implicada para dialogar sobre la situación e invitarla a retomar su participación.
2. Si, tras un tiempo razonable, la persona sigue sin mostrar actividad o intención de contribuir al proyecto:
   - Se informará al profesor para que gestione la posible baja del miembro en cuestión.

## **Conflicto: Retraso significativo en la entrega de una tarea**
### **Solución:**
1. Si un miembro tiene dificultades para completar una tarea, deberá:
   - Notificarlo al equipo lo antes posible.
   - Explicar las causas del bloqueo.
   - Solicitar ayuda de uno o más compañeros si es necesario.
2. Si no se informa del problema con antelación y esto resulta en un retraso que afecta negativamente al proyecto:
   - Se aplicará una reducción en los puntos de implicación asignados a dicho miembro.

## **Conflicto: Diferencias de opinión sobre temas del trabajo**
### **Solución:**
1. Las diferencias de opinión se resolverán internamente mediante diálogo y búsqueda de consenso entre los miembros del equipo.
2. En casos extremos, si no se logra un acuerdo, se recurrirá al coordinador del proyecto para que actúe como mediador.

## **Conflicto: Un miembro no sigue las políticas de desarrollo del equipo**
### **Solución:**
1. Se informará al miembro sobre las políticas de desarrollo que no está cumpliendo, recordándole la importancia de seguir las normas acordadas por el equipo.
2. Si persiste en aplicar su propia metodología y no se adapta a las políticas del equipo:
   - Se informará al tutor, quien evaluará la situación. Esto podría resultar en una reducción de la calificación del miembro afectado.

## **Propósito de estas Políticas**
Estas medidas están diseñadas para:
- Fomentar la comunicación y la colaboración.
- Resolver conflictos de forma constructiva y justa.
- Mantener la calidad y el ritmo de trabajo del proyecto.

Al seguir estas directrices, buscamos garantizar un entorno de trabajo productivo y respetuoso para todos los miembros del equipo.


<div id='id9'></div>


# 9. Gestión de Incidencias

En nuestro proyecto, las incidencias se gestionan mediante la creación de **issues** en el repositorio de GitHub, siguiendo un proceso claro y estructurado. Esto permite una resolución eficiente y facilita el seguimiento de problemas en el sistema.

## **Proceso de Gestión de Incidencias**
### **1. Creación de la Issue**
- Cuando se detecta una incidencia, se crea una nueva **issue** en GitHub.
- La issue debe incluir:
  - **Título descriptivo**: Un resumen breve del problema.
  - **Etiqueta**: Se debe asignar la etiqueta `bug` para identificarla como una incidencia.
  - **Descripción detallada**:
    - **En inglés**, siguiendo el estándar del proyecto.
    - Debe incluir los pasos para reproducir el problema y una descripción clara de los síntomas.

### **2. Estructura de la Descripción**
La descripción de la issue debe incluir los siguientes puntos:

1. **Descripción del problema**:
   - Explica qué ocurre y dónde se manifiesta el problema.
   - Incluye capturas de pantalla o logs si son relevantes.

2. **Pasos para resolver la incidencia**:
   - Lista detallada y numerada con los pasos a seguir para investigar y resolver el problema.
   - Especifica los cambios necesarios y cómo verificarlos.

**Ejemplo de Issue**:  
**Título**: Fix Communities Locust Tests  
**Descripción**:  
```plaintext
When you try to run Locust tests for the community module with the rosemary locust community, the Host field appears empty.
```

**Steps to resolve:**
1. Analyze the scope of the issue:
    - Verify why the Host field appears empty in the Locust interface.
    - Confirm if the issue is related to the host attribute in the test class or the structure of the test file.
    - Test similar configurations to ensure the issue is isolated to community tests.
2. Create a new branch named fix/communities_locust_tests.
3. Debug the test file:
    - Check if the `host` attribute is defined in the `CommunityUser` class.
    - Verify the naming convention of the test file to ensure Locust recognizes it automatically.
4. Implement fixes:
    - Add `host = get_host_for_locust_testing()` to the `CommunityUser` class.
    - Rename the test file to comply with Locust's naming convention.
5. Test the fix locally:
    - Run Locust locally to confirm the Host field is populated correctly.
    - Verify that the tests run successfully.
6. Validate the fix with Docker:
    - Execute Locust tests in the Docker environment to ensure deployment works as expected.
7. Commit and push changes:
    - Commit with a descriptive message: "Fix Locust tests for community: added host and renamed file."
8. Create a Pull Request:
    - Open a PR to `main` and include a summary of the problem and the solution.
9. Verify after merge:
    - Pull the latest changes from `main` and confirm the issue is resolved.
10. Document and close the issue:
    - Update the issue tracker with a summary of the fix and close the issue.

### 3. **Resolución y Seguimiento**:

  - Cada issue es asignada a uno o más miembros del equipo responsables de su resolución.
  - Una vez solucionada la incidencia, el responsable debe:
    - Documentar los pasos realizados en la issue.
    - Verificar que la solución funciona correctamente.
    - Cerrar la issue tras confirmar que el problema ha sido resuelto.

### 4. **Buenas Prácticas**:
- Lenguaje: Toda la documentación técnica de las issues (como los pasos para resolverlas) debe estar en inglés, alineándose con el estándar del proyecto.
- Claridad: Los pasos deben ser detallados y comprensibles para facilitar la resolución por cualquier miembro del equipo.
- Estandarización: Asegurarse de que todas las issues sigan un formato similar para mantener un sistema de seguimiento coherente y profesional.

Con esta política, aseguramos una gestión eficiente de incidencias que facilita su resolución y mejora la calidad del proyecto.