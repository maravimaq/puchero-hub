#!/bin/bash

project_root=$(dirname "$(dirname "$(realpath "$0")")")
requirements_file="$project_root/requirements.txt"

echo "🔄 Verificando e instalando la última versión de pip..."
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip

if [[ ! -f "$requirements_file" ]]; then
  echo "❌ No se encontró el archivo $requirements_file. Asegúrate de que exista."
  exit 1
fi

echo "📄 Leyendo dependencias desde $requirements_file..."

while IFS= read -r dependency || [ -n "$dependency" ]; do
  if [[ -z "$dependency" || "$dependency" =~ ^# ]]; then
    continue
  fi

  echo "🔍 Verificando $dependency..."
  package_name=$(echo "$dependency" | cut -d'=' -f1)
  python3 -m pip show "$package_name" &> /dev/null

  if [[ $? -eq 0 ]]; then
    echo "✔ $dependency ya está instalado. Se omite."
  else
    echo "➤ Instalando $dependency..."
    python3 -m pip install "$dependency"
    if [[ $? -ne 0 ]]; then
      echo "❌ Error al instalar $dependency. Revisa el archivo requirements.txt."
      exit 1
    fi
  fi
done < "$requirements_file"

echo "🎉 Todas las dependencias han sido revisadas o instaladas correctamente."
