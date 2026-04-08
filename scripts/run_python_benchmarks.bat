@echo off
chcp 65001 >nul
REM Script para ejecutar el benchmark de Python en Windows

echo ==========================================
echo TALLER - Benchmark Python
echo Algoritmos de Ordenamiento y Busqueda
echo ==========================================
echo.

REM Obtener directorio del script
set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%.."
set "PYTHON_DIR=%PROJECT_DIR%\src\python"

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    exit /b 1
)

echo [OK] Python encontrado
python --version
echo.

REM Cambiar al directorio de Python
cd /d "%PYTHON_DIR%"

REM Verificar dependencias
echo Verificando dependencias...
python -c "import matplotlib, seaborn, pandas, numpy" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] No se pudieron instalar las dependencias
        exit /b 1
    )
) else (
    echo [OK] Dependencias verificadas
)
echo.

REM Ejecutar benchmark completo
echo ==========================================
echo INICIANDO BENCHMARK COMPLETO
echo ==========================================
echo.

python main_completo.py -i "../../data/input" -o "../../data/output" -g "../../docs/graficos"

if errorlevel 1 (
    echo.
    echo [ERROR] El benchmark fallo
    exit /b 1
)

echo.
echo ==========================================
echo BENCHMARK COMPLETADO EXITOSAMENTE
echo ==========================================
echo.
echo Resultados guardados en:
echo   - data/output/resultados_python.csv
echo   - data/output/resultados_python.json
echo.
echo Graficos guardados en:
echo   - docs/graficos/comparacion_ordenamiento.png
echo   - docs/graficos/comparacion_busqueda.png
echo   - docs/graficos/comparacion_por_tamaño.png
echo.

pause