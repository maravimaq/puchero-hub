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

## Índice.
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
7. [Gestión de Conflictos](#id7)
8. [Gestión de Incidencias](#id8)


<div id='id1'></div>


## 1. Miembros de puchero-hub.
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


## 2. ¿Qué es Puchero-hub?
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


## 3. Roles del equipo.
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


## 4. Repositorio en GitHub.
Nuestro proyecto se ha realizado subiendo dicho proyecto a un repositorio común en la plataforma GitHub. Este repositorio es el siguiente: [Puchero-hub](https://github.com/maravimaq/puchero-hub.git).

### i. Estructura del repositorio.
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


## 5. Políticas
En esta sección vamos a hablar de las distintas políticas a seguir por el equipo. Estas políticas son políticas decididas por el conjunto del equipo, y deben ser acatadas por todos los miembros de este.

<div id='id51'></div>

### i. Política de Commits.
Nuestro equipo sigue una política de commits que se llama **Conventional Commits**. # Política de Commits: Conventional Commits

La política **Conventional Commits** es un estándar ampliamente utilizado para redactar mensajes de commits de manera clara y estructurada. Su objetivo principal es mantener un historial consistente y fácil de entender, facilitando el trabajo en equipo, la revisión de cambios y el uso de herramientas automatizadas como generación de changelogs y versionado semántico.

#### **Estructura del Mensaje de Commit**

Cada mensaje de commit debe seguir la siguiente estructura:

```plaintext
<tipo>(<alcance opcional>): <descripción breve>
```

- **`tipo`**: Describe el propósito del cambio. Por ejemplo: `feat`, `fix`, `docs`, etc.
- **`alcance` (opcional)**: Especifica el módulo, componente o área afectada del proyecto. Por ejemplo: `(login)`, `(API)`.
- **`descripción breve`**: Explica de manera concisa qué se ha hecho.

#### Tipos de Commits

A continuación, se describen los principales tipos de commits que seguimos en este proyecto:

##### `feat`: Funcionalidades nuevas
- **Uso**: Commits que añaden nuevas funcionalidades o crean nuevos archivos.
- **Ejemplo**:  

```plaintext
feat(login): añadir autenticación de usuarios
```

##### `fix`: Correcciones de errores
- **Uso**: Commits que corrigen fallos o errores en el código.
- **Ejemplo**: 

```plaintext
fix(api): corregir error de validación en el endpoint de usuarios
```

##### `docs`: Documentación
- **Uso**: Commits relacionados con cambios en la documentación, como manuales o README.
- **Ejemplo**:  

```plaintext
docs(readme): actualizar requisitos de instalación
```

##### `test`: Pruebas
- **Uso**: Commits que contienen cambios o adiciones en las pruebas, como unitarias o de integración.
- **Ejemplo**:  

```plaintext
test(auth): añadir pruebas para la autenticación de usuarios
```

#### Ventajas de Usar Conventional Commits

- **Consistencia**: Los mensajes son uniformes, lo que facilita la lectura del historial de commits.
- **Automatización**: Se pueden generar changelogs automáticos y realizar versionado semántico.
- **Colaboración**: Facilita la comunicación dentro del equipo sobre los cambios realizados.

Esta política asegura que cada commit refleje de manera precisa el trabajo realizado y permite un mejor mantenimiento del proyecto a lo largo del tiempo.

<div id='id52'></div>

### ii. Política de Ramas.
En nuestro proyecto seguimos el flujo de trabajo **Feature Branch Workflow**, el cual permite un desarrollo organizado y colaborativo. A continuación, se detalla el proceso que seguimos para gestionar las ramas:

#### **1. Creación de ramas independientes**
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

#### **2. Desarrollo en las ramas independientes**
- Todo el desarrollo relacionado con la funcionalidad o corrección específica se realiza dentro de la rama creada.
- Esto asegura que la rama principal (`main`) permanezca siempre estable y lista para su uso.

#### **3. Creación de una Pull Request**
- Una vez completado el desarrollo en la rama independiente, se crea una **Pull Request (PR)** hacia la rama principal (`main`).
- En la PR, se describen los cambios realizados y se incluye cualquier información relevante.

#### **4. Revisión por parte del equipo**
- Nosotros hemos implementado que no haga falta revisión por parte del equipo, ya que eso consideramos que provoca retrasos a la hora de realizar el proyecto.
- Como único requisito de revision tenemos que no se suba nada que de error, o fallo. Todo lo que se suba al repositorio debe ser funcional.

#### **5. Fusión con la rama principal**
- La Pull Request será **mergeada** con la rama `main`.

#### **6. Eliminación de la rama**
- Después de la fusión, la rama de funcionalidad puede ser **eliminada** para mantener el repositorio limpio y organizado.
- No tenemos la obligación impuesta de eliminar o no la rama. Hay libertad en este aspecto.

#### **Ventajas de esta política**
- **Colaboración efectiva**: La revisión por parte de otros desarrolladores mejora la calidad del código.
- **Estructura clara**: Las ramas independientes organizan el trabajo y protegen la estabilidad de `main`.
- **Control de calidad**: Solo los cambios revisados y aprobados llegan a `main`.

Con esta política, aseguramos un flujo de trabajo eficiente, colaborativo y de alta calidad en el desarrollo de nuestro proyecto.


<div id='id53'></div>


### iii.Política de Issues.
Nuestro equipo ha decidido no seguir una política de Issues específica en cuanto al nombramiento de estas. Básicamente, los nombres de estas van a seguir un formato de explicación descriptiva de la Issue, y en inglés.

A cada Issue se le asignará una etiqueta según sobre el tipo de issue que sea. Para ello vamos a usar las etiquetas dadas por defecto en github, junto a la adición de una nueva, que recibe el nombre `test`. Esta última no se encuentra en github, y la vamos a usar para las issues dedicadas a las pruebas.

Además, para el uso y empleo detallado de las issues, hemos usado la extensión y plataforma Zenhub, la cuál mediante un tablero nos permite conectar las issues a las pull requests, y que en este tablero, se desplacen automáticamente al estar conectadas, y tras realizar una pull request sobre esa issue.

Por último, se ha tomado la decisión de que las Issues se agruparán en Épicas para así mantener una organización más específica y detallada.


<div id='id54'></div>


### iv. Política de Versionado.
