# Documentación de los fallos arreglados en los tests

## test_delete_nonexistent_or_unauthorized_community

### Alcance del problema
El test fallaba porque no se validaba correctamente el mensaje flash `"Community not found or you do not have permission to delete it."` al intentar eliminar una comunidad inexistente o no autorizada.

### Verificación del problema
Se verificó que el problema no estaba aislado a una plantilla específica, sino que estaba relacionado con la lógica del backend y la falta de validación del mensaje flash.

### Corrección aplicada
1. Se agregó una validación en el test para comprobar que el mensaje flash correcto estaba presente en la sesión (`_flashes`).
2. Se simuló el acceso no autorizado para confirmar que el backend generaba el mensaje esperado.

### Estado después de la corrección
El test ahora pasa correctamente y valida que el mensaje flash se muestra al intentar eliminar comunidades inexistentes o no autorizadas.

---

## test_edit_nonexistent_or_unauthorized_community

### Alcance del problema
El test fallaba porque no se verificaba correctamente el mensaje flash `"Community not found or you do not have permission to edit it."` al intentar editar una comunidad inexistente o no autorizada.

### Verificación del problema
Se probó que el problema no era exclusivo de la plantilla `edit.html`, sino que estaba relacionado con la lógica del backend y la redirección.

### Corrección aplicada
1. Se añadió una verificación del mensaje flash directamente en la sesión para confirmar que el mensaje se generaba al intentar editar comunidades inexistentes o no autorizadas.

### Estado después de la corrección
El test ahora pasa y confirma que el mensaje flash se genera y se muestra correctamente.

---

## test_show_nonexistent_community

### Alcance del problema
El test fallaba porque no se validaba correctamente el mensaje flash `"Community not found."` al intentar visualizar una comunidad inexistente.

### Verificación del problema
Se verificó que el problema estaba relacionado con la lógica del backend y no con la plantilla `show.html`, que ya tenía el bloque para mensajes flash.

### Corrección aplicada
1. Se añadió una validación del mensaje flash desde la sesión para confirmar que se generaba correctamente.
2. Se revisó que el backend manejara la redirección adecuada y generara el mensaje esperado.

### Estado después de la corrección
El test ahora pasa correctamente y valida que el mensaje flash se muestra al intentar acceder a una comunidad inexistente.

---

## test_delete_community_success

### Alcance del problema
El test fallaba porque no se validaba correctamente el mensaje flash `"Community deleted successfully!"` al eliminar una comunidad con éxito.

### Verificación del problema
Se verificó que el problema estaba relacionado con la falta de validación explícita del mensaje flash en el test, no con la plantilla.

### Corrección aplicada
1. Se agregó una validación del mensaje flash desde la sesión para confirmar que el backend generaba el mensaje al eliminar una comunidad.
2. Se probó el flujo completo para asegurarse de que el mensaje de éxito aparecía en el HTML.

### Estado después de la corrección
El test ahora pasa correctamente y valida que el mensaje de éxito se genera y se muestra al eliminar comunidades.

---

## test_create_community_error_handling

### Alcance del problema
El test fallaba porque no se validaba correctamente el mensaje flash `"Error creating community."` al simular un fallo en la creación de una comunidad.

### Verificación del problema
Se verificó que el problema estaba relacionado con la lógica del backend y la necesidad de manejar los errores correctamente en el bloque `try` del método `create_community`.

### Corrección aplicada
1. Se añadió un mock para simular un fallo en `db.session.add` y validar que el mensaje flash se generaba correctamente.
2. Se validó que el bloque para renderizar mensajes flash estuviera presente en la plantilla `create.html`.

### Estado después de la corrección
El test ahora pasa correctamente y valida que el mensaje flash aparece en caso de error durante la creación de comunidades.

---

## Pasos seguidos para resolver los fallos

1. **Analizar el alcance del problema**  
   Se verificó si el fallo era específico de una plantilla o de la lógica del backend.  
   Se revisaron rutas similares (`edit`, `delete`, `show`) para confirmar si el problema era aislado o general.

2. **Crear una nueva rama**  
   Se creó una rama llamada `fix/community_flash_messages` para aplicar los arreglos.

3. **Depurar las plantillas**  
   Se verificó que las plantillas (`create.html`, `edit.html`, `my_communities.html`) incluyeran el bloque para mensajes flash.

4. **Probar la solución localmente**  
   Se simuló un fallo en los métodos de backend (`create`, `edit`, `delete`) para comprobar que los mensajes flash aparecieran correctamente en el UI.

5. **Validar la solución con tests**  
   Se actualizaron los tests para incluir validaciones de mensajes flash desde la sesión (`_flashes`).

6. **Hacer commit y push de los cambios**  
   Se realizó un commit con los cambios realizados.

7. **Crear un Pull Request**  
   Se abrió un PR desde la rama `fix/community_flash_messages` hacia `main`, incluyendo el número del issue y un resumen de la solución.

8. **Verificar tras el merge**  
   Se fusionó el PR y se verificó que los cambios solucionaran los problemas en la rama `main`.

9. **Documentar la resolución**  
   Se actualizaron los registros del issue tracker con los pasos tomados y se cerró el issue tras verificar la solución.

---

