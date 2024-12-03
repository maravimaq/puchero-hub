# Documentación de Fallos Arreglados en los Tests

## **test_pack_datasets_no_uploads_folder**

### **Alcance del Problema**

El test fallaba porque la función `pack_datasets` no manejaba correctamente el caso en el que la carpeta `uploads` no existía. En lugar de devolver `None`, creaba archivos temporales innecesarios.

### **Verificación del Problema**

- Se verificó que el fallo estaba aislado a la ausencia de la carpeta `uploads`.

### **Corrección Aplicada**

- Se actualizó la lógica en `pack_datasets` para que devuelva `None` inmediatamente si la carpeta `uploads` no existe.

### **Estado Tras la Corrección**

- El test ahora pasa correctamente y confirma que la función `pack_datasets` se comporta como se espera cuando falta la carpeta `uploads`.

---

## Pasos Seguidos para Resolver el Problema del Test

1. **Analizar el alcance del problema**  

   Se determinó que el fallo estaba relacionado con la lógica del backend en la función `pack_datasets`, y no con la configuración del test.

2. **Crear una nueva rama**  

   Se creó una rama llamada `fix/pack_datasets_no_uploads` para abordar el problema.

3. **Depurar la función**  

   Se utilizó logging y debugging para verificar que la función `pack_datasets` no devolvía `None` de forma temprana cuando la carpeta `uploads` no existía.

4. **Actualizar la lógica de la función** 

   Se ajustó la función para que devuelva `None` inmediatamente si la carpeta `uploads` no está presente, y se garantizó que no se crearan archivos innecesarios.

5. **Probar la solución localmente**  

   Se simularon los siguientes escenarios:

   - La carpeta `uploads` no existe.

   - La carpeta `uploads` existe pero no contiene carpetas de usuario ni datasets.

   - Existen datasets válidos en la carpeta `uploads`.

6. **Validar con pruebas actualizadas** 

   - Se mejoraron los tests para incluir casos límite.

   - Se verificó que no se crearan archivos temporales innecesarios.

7. **Hacer commit y push de los cambios** 

   Se realizó un commit con el mensaje: `"Fix(datasets): Added new validation to pack_datasets, to make sure it doesn't return anything when there is not uploads folder"`

8. **Crear un Pull Request**  

   Se abrió un PR desde `fix/pack_datasets_no_uploads` hacia `main`, incluyendo la referencia del issue y un resumen de la solución.

9. **Verificar tras el merge**  

   Tras la fusión del PR, se probó la funcionalidad en la rama `main` para confirmar que el problema estaba resuelto.

10. **Documentar la solución**  

    Se actualizó el tracker del issue con los pasos seguidos y se cerró el issue tras confirmar la corrección.

---
