#!/bin/bash
# Script para ejecutar el benchmark de Python en Linux/Mac

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON_DIR="$PROJECT_DIR/src/python"

echo "=========================================="
echo "TALLER - Benchmark Python"
echo "Algoritmos de Ordenamiento y Búsqueda"
echo "=========================================="
echo

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 no está instalado"
    exit 1
fi

echo "[OK] Python encontrado"
python3 --version
echo

# Cambiar al directorio de Python
cd "$PYTHON_DIR"

# Verificar dependencias
echo "Verificando dependencias..."
if python3 -c "import matplotlib, seaborn, pandas, numpy" 2>/dev/null; then
    echo "[OK] Dependencias verificadas"
else
    echo "Instalando dependencias..."
    pip3 install -r requirements.txt
fi
echo

# Ejecutar benchmark completo
echo "=========================================="
echo "INICIANDO BENCHMARK COMPLETO"
echo "=========================================="
echo

python3 main_completo.py -i "../../data/input" -o "../../data/output" -g "../../docs/graficos"

echo
echo "=========================================="
echo "BENCHMARK COMPLETADO EXITOSAMENTE"
echo "=========================================="
echo
echo "Resultados guardados en:"
echo "  - data/output/resultados_python.csv"
echo "  - data/output/resultados_python.json"
echo
echo "Gráficos guardados en:"
echo "  - docs/graficos/comparacion_ordenamiento.png"
echo "  - docs/graficos/comparacion_busqueda.png"
echo "  - docs/graficos/comparacion_por_tamaño.png"
echo