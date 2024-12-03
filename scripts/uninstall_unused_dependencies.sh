#!/bin/bash

REQUIREMENTS_FILE="../requirements.txt"

if [[ ! -f "$REQUIREMENTS_FILE" ]]; then
    echo "❌ No se encontró el archivo $REQUIREMENTS_FILE. Por favor, asegúrate de que existe."
    exit 1
fi

echo "📄 Leyendo dependencias desde $REQUIREMENTS_FILE..."

pip install packaging > /dev/null 2>&1

declare -A REQUIRED_DEPENDENCIES
while IFS= read -r line || [ -n "$line" ]; do
    if [[ -z "$line" || "$line" =~ ^# ]]; then
        continue
    fi

    PACKAGE=$(echo "$line" | awk -F'[><=]' '{print $1}')
    SPECIFIER=$(echo "$line" | awk -F"$PACKAGE" '{print $2}')
    REQUIRED_DEPENDENCIES["$PACKAGE"]="$SPECIFIER"
done < "$REQUIREMENTS_FILE"

echo "🔍 Comparando dependencias instaladas con las requeridas..."

INSTALLED_DEPENDENCIES=$(pip list --format=freeze)

while IFS= read -r installed_dep || [ -n "$installed_dep" ]; do
    INSTALLED_PACKAGE=$(echo "$installed_dep" | cut -d'=' -f1)
    INSTALLED_VERSION=$(echo "$installed_dep" | cut -d'=' -f2-)

    if [[ -n "${REQUIRED_DEPENDENCIES[$INSTALLED_PACKAGE]}" ]]; then
        REQUIRED_SPECIFIER="${REQUIRED_DEPENDENCIES[$INSTALLED_PACKAGE]}"
        python3 -c "
from packaging.specifiers import SpecifierSet
from packaging.version import Version

spec = SpecifierSet('$REQUIRED_SPECIFIER')
if not Version('$INSTALLED_VERSION') in spec:
    print('UPDATE')
" 2>/dev/null && {
            echo "⚠ Versión no coincide para $INSTALLED_PACKAGE: instalada $INSTALLED_VERSION, requerida ${REQUIRED_DEPENDENCIES[$INSTALLED_PACKAGE]}"
            pip install "$INSTALLED_PACKAGE${REQUIRED_DEPENDENCIES[$INSTALLED_PACKAGE]}"
        }
    else
        echo "✔ $INSTALLED_PACKAGE cumple con los requisitos. Se omite."
    fi
done <<< "$INSTALLED_DEPENDENCIES"

echo "🎉 Limpieza completada. Todas las dependencias están sincronizadas con $REQUIREMENTS_FILE."
