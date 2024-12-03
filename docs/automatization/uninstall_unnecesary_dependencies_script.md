# Documentación de Scripts

## 2. Script: `uninstall_unused_dependencies.sh`

### Propósito

Eliminar las dependencias instaladas que no estén listadas en el archivo `requirements.txt` o cuya versión no coincida con la especificada en el archivo.

### Ubicación esperada

`/scripts/uninstall_unused_dependencies.sh`

---

### Funcionamiento paso a paso

1. **Lectura del archivo `requirements.txt`**  

   Crea una lista de las dependencias permitidas y sus versiones especificadas en el archivo.

2. **Listado de dependencias instaladas**  

   Obtiene todas las dependencias actualmente instaladas en el entorno virtual.

3. **Comparación y desinstalación**  

   Identifica las dependencias que no están en `requirements.txt` o cuyas versiones no coinciden, y procede a desinstalarlas.

---

### Código del script

```bash
#!/bin/bash

echo "📄 Leyendo dependencias desde ../requirements.txt..."
REQUIREMENTS_FILE="../requirements.txt"
ALLOWED_DEPENDENCIES=$(awk '!/^#/ && NF {print $1}' "$REQUIREMENTS_FILE")

echo "🔍 Comparando dependencias instaladas con las requeridas..."
for PACKAGE in $(pip freeze | awk -F'==' '{print $1}'); do
  if ! grep -q "$PACKAGE" <<< "$ALLOWED_DEPENDENCIES"; then
    echo "❌ $PACKAGE no está en $REQUIREMENTS_FILE. Desinstalando..."
    pip uninstall -y "$PACKAGE"
  fi
done

echo "🎉 Limpieza completada. Todas las dependencias están sincronizadas con $REQUIREMENTS_FILE."
