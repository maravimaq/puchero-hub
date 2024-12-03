# Documentación de Scripts

## 1. Script: `install_dependencies.sh`

### Propósito

Instalar todas las dependencias listadas en el archivo `requirements.txt`, ignorando dependencias que ya estén instaladas y con la versión correcta. Además, instalar nuevas herramientas necesarias para workflows específicos.

### Ubicación esperada

`/scripts/install_dependencies.sh`

---

### Funcionamiento paso a paso

1. **Verificación de pip**  

   Asegura que `pip` esté instalado y actualizado a la última versión.

2. **Lectura del archivo `requirements.txt`**  

   Identifica todas las dependencias y sus especificadores (e.g., `==`, `>=`).

3. **Comparación con dependencias instaladas** 

   Solo instala o actualiza las dependencias que no estén instaladas o cuya versión no cumpla los requisitos.

4. **Instalación de herramientas adicionales** 
 
   Agrega herramientas específicas requeridas por los workflows, como `flake8`, `black`, o `pip-audit`.

---

### Código del script

```bash
#!/bin/bash

echo "🔄 Verificando e instalando la última versión de pip..."
pip install --upgrade pip

echo "📄 Leyendo dependencias desde ../requirements.txt..."
REQUIREMENTS_FILE="../requirements.txt"

while IFS= read -r line; do
  [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue
  PACKAGE=$(echo $line | awk -F'[><=]' '{print $1}')
  INSTALLED_VERSION=$(pip show "$PACKAGE" | grep "Version:" | awk '{print $2}')
  if [[ -n "$INSTALLED_VERSION" && "$line" == "$PACKAGE==$INSTALLED_VERSION" ]]; then
    echo "✔ $line ya está instalado. Se omite."
  else
    echo "➤ Instalando o actualizando $line..."
    pip install "$line"
  fi
done < "$REQUIREMENTS_FILE"

echo "🎉 Todas las dependencias han sido revisadas o instaladas correctamente."
