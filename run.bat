@echo off
chcp 65001 >nul

echo ============================================================
echo     Ejecutar Programa - Taller Algoritmos
echo     Java + Python Benchmark
echo ============================================================
echo.

set BIN_DIR=bin
set MAIN_CLASS=org.algoritmos.main.MainCompleto
set PYTHON_SCRIPT=src\python\main_completo.py
set INPUT_DIR=data\input
set OUTPUT_DIR=data\output
set GRAFICOS_DIR=docs\graficos

:: ============================================
:: PASO 1: Ejecutar Java
:: ============================================
echo.
echo [PASO 1/2] Ejecutando MainCompleto.java...
echo -----------------------------------------------------------

if not exist %BIN_DIR% (
    echo ERROR: Directorio %BIN_DIR% no encontrado.
    echo Ejecuta build.bat primero para compilar.
    pause
    exit /b 1
)

:: Ejecutar Java desde el directorio raiz para que use las carpetas data de raiz
java -cp %BIN_DIR% %MAIN_CLASS%
if errorlevel 1 (
    echo ERROR: La ejecucion de Java fallo.
    pause
    exit /b 1
)

echo.
echo [OK] Java finalizado correctamente.
echo -----------------------------------------------------------

:: ============================================
:: PASO 2: Ejecutar Python
:: ============================================
echo.
echo [PASO 2/2] Ejecutando benchmark Python...
echo -----------------------------------------------------------

:: Verificar que Python este instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en PATH.
    echo Por favor, instala Python para ejecutar el benchmark.
    pause
    exit /b 1
)

echo Python detectado:
python --version

:: Verificar que el script Python exista
if not exist %PYTHON_SCRIPT% (
    echo ERROR: Script Python no encontrado: %PYTHON_SCRIPT%
    pause
    exit /b 1
)

:: Crear directorios de salida si no existen
if not exist %OUTPUT_DIR% mkdir %OUTPUT_DIR%
if not exist %GRAFICOS_DIR% mkdir %GRAFICOS_DIR%

:: Ejecutar Python desde el directorio raiz
echo.
echo Ejecutando: %PYTHON_SCRIPT%
echo Input:  %INPUT_DIR%
echo Output: %OUTPUT_DIR%
echo Graficos: %GRAFICOS_DIR%
echo.

python %PYTHON_SCRIPT% --input %INPUT_DIR% --output %OUTPUT_DIR% --graficos %GRAFICOS_DIR%
if errorlevel 1 (
    echo ERROR: La ejecucion de Python fallo.
    pause
    exit /b 1
)

echo.
echo [OK] Python finalizado correctamente.
echo -----------------------------------------------------------

:: ============================================
:: FINALIZACION
:: ============================================
echo.
echo ============================================================
echo     Ejecucion completada exitosamente
echo     - Java: Resultados en consola
echo     - Python: Graficos en %GRAFICOS_DIR%
echo ============================================================
echo.
pause
