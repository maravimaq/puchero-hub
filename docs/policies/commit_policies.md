
# Plantilla para Commits en el Proyecto

Esta plantilla define el formato estándar que deben seguir los mensajes de commit en este proyecto. Utilizarla asegura claridad, consistencia y facilidad para entender los cambios realizados.

---

## Tipos de Commits (Types)

### **Feat:**

- Descripción: Breve descripción de lo hecho.

- Uso: Para commits que añaden nuevas funcionalidades o crean nuevos archivos.

### **Fix:**

- Descripción: Breve descripción de lo hecho.

- Uso: Para commits que corrigen fallos o errores en el proyecto.

### **Docs:**

- Descripción: Breve descripción de lo hecho.

- Uso: Para commits relacionados con la documentación (README, comentarios, etc.).

### **Test:**

- Descripción: Breve descripción de lo hecho.

- Uso: Para commits relacionados con las pruebas unitarias, de integración u otras.

---

## Estructura del Mensaje de Commit

```plaintext
<Tipo>(<Contexto>): Breve descripción del cambio realizado

Descripción más detallada (opcional):
- Explica qué problema resolviste o qué funcionalidad agregaste.
- Incluye cualquier información adicional necesaria.

Notas (opcional):
- Relacionado con: #<Número de issue o tarea>
- Dependencias o cambios que pueden afectar otras partes del sistema.
```

---

## Ejemplo de Commit

### **1. Feat (Nueva funcionalidad):**

```plaintext
feat(auth): Añadida funcionalidad de login con autenticación OAuth

- Implementación de login utilizando el proveedor de Google.

- Se añadieron nuevas rutas y controladores.

- Documentación actualizada para describir la funcionalidad.

Notas:
- Relacionado con: #123
```

### **2. Fix (Corrección de errores):**

```plaintext
fix(api): Corregido error en la validación de los datos del usuario

- Se corrigió un problema donde los datos no eran validados correctamente.

- Ajustes realizados en los controladores y pruebas correspondientes.

Notas:
- Relacionado con: #456
```

### **3. Docs (Documentación):**

```plaintext
docs(readme): Actualizada la sección de instalación del proyecto

- Instrucciones revisadas para reflejar los cambios en las dependencias.

- Añadidos ejemplos de configuración para entornos locales.

Notas:
- Relacionado con: #789
```

### **4. Test (Pruebas):**

```plaintext
test(api): Añadidas pruebas unitarias para las nuevas validaciones

- Se crearon casos de prueba para validar datos de usuarios.

- Cobertura de pruebas aumentada al 95%.

Notas:
- Relacionado con: #321
```

---

## Cómo Configurar la Plantilla

1. Guarda este archivo como `commit_template.txt` en la carpeta `docs` del proyecto.

2. Configura Git para usar la plantilla:
   ```bash
   git config commit.template ./docs/commit_template.txt
   ```

---