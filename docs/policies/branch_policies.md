
# Política de Gestión de Ramas

Esta política describe el modelo de uso y las reglas para la gestión de ramas en el proyecto, asegurando un flujo de trabajo eficiente y organizado.

---

## **Modelo de Uso**

1. **Rama principal (`main`)**:

   - Se utiliza como la rama principal para la integración continua (CI).

2. **Ramas para nuevas funcionalidades**:

   - Para cada nueva funcionalidad o tarea, se crea una rama específica con el formato: `feature/<nombre-de-la-feature>`.

3. **Ramas para corrección de bugs**:

   - Las ramas destinadas a solucionar errores existentes siguen el formato: `fix/<nombre-de-la-tarea>`.

4. **Proceso de integración**:

   - Una vez finalizado el trabajo en una rama específica, se crea un **pull request** para integrar los cambios en la rama `main`.

   - Después de integrar los cambios, la rama específica se elimina para mantener el repositorio limpio.

5. **Frecuencia de merges**:

   - Se intenta realizar al menos un merge a la rama `main` por semana.

---

## **Definición de Hecho (Definition of Done - DoD)**

Para considerar un merge como completo, deben cumplirse las siguientes condiciones:

1. **Sin errores**:

   - El código debe estar libre de errores y cumplir con el resultado esperado.

2. **Revisión del equipo**:

   - **Cambios complejos**: Si la funcionalidad es compleja o puede causar un fallo considerable, debe ser revisada y aprobada por al menos un miembro del equipo antes de aceptar el pull request.

   - **Cambios simples**: Cambios pequeños con poco impacto (como documentación o funcionalidades simples) pueden mergearse sin necesidad de revisión.

3. **Pruebas exitosas**:

   - Los sets de pruebas (unitarias e integración) deben ejecutarse sin fallos.

4. **Cumplimiento de estándares de calidad (Codacy)**:

   - Los cambios deben pasar los estándares de calidad establecidos por Codacy.

   - Si existe un motivo para realizar el merge sin cumplir estos estándares, este debe explicarse en un comentario en el pull request.

---

## **Resumen del Flujo de Trabajo**

1. Crear una rama específica (`feature/<nombre>` o `fix/<nombre>`).

2. Realizar el desarrollo o corrección en la rama.

3. Asegurarse de que el código cumple con las condiciones de la **Definición de Hecho (DoD)**.

4. Crear un pull request para integrar los cambios en `main`.

5. Revisar el pull request según las reglas establecidas.

6. Realizar el merge a `main` si se cumplen todas las condiciones.

7. Eliminar la rama específica una vez completado el merge.