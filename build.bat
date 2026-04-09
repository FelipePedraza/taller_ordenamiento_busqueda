@echo off
chcp 65001 >/dev/null
cls

echo ============================================================
echo   Script de Compilacion - Taller Algoritmos Java + Python
echo ============================================================
echo.

set SRC_DIR=src\java
set BIN_DIR=bin
set MAIN_CLASS=org.algoritmos.main.MainCompleto
set PYTHON_SCRIPT=src\python\main_completo.py
set INPUT_DIR=data\input
set OUTPUT_DIR=data\output
set GRAFICOS_DIR=docs\graficos

echo [1/5] Limpiando directorio de salida...
if exist %BIN_DIR% (
    rmdir /s /q %BIN_DIR%
)
mkdir %BIN_DIR%
echo     Directorio %BIN_DIR% listo
echo.

echo [2/5] Compilando archivos Java...
javac -d %BIN_DIR% -encoding UTF-8 -sourcepath %SRC_DIR% %SRC_DIR%\org\algoritmos\util\*.java %SRC_DIR%\org\algoritmos\ordenamiento\*.java %SRC_DIR%\org\algoritmos\busqueda\*.java %SRC_DIR%\org\algoritmos\main\*.java

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR de compilacion
    pause
    exit /b 1
)

echo     Compilacion exitosa
echo.

echo [3/5] Verificando compilacion...
set /a count=0
for /r %BIN_DIR% %%f in (*.class) do set /a count+=1
echo     %count% clases compiladas
echo.

echo [4/5] Ejecutando programa Java...
echo ------------------------------------------------------------

:: Ejecutar Java desde el directorio raiz para que use las carpetas data de raiz
java -cp %BIN_DIR% %MAIN_CLASS%
set RESULT=%ERRORLEVEL%

echo ------------------------------------------------------------

if %RESULT% equ 0 (
    echo Ejecucion Java completada exitosamente
) else (
    echo ERROR durante la ejecucion Java (codigo: %RESULT%)
)

echo.

echo [5/5] Ejecutando benchmark Python...
echo ------------------------------------------------------------
echo.

:: Verificar que Python este instalado
python --version >/dev/null 2>&1
if %ERRORLEVEL% neq 0 (
    echo WARNING: Python no esta instalado o no esta en el PATH
    echo No se ejecutara el benchmark de Python
    echo.
    echo Para instalar Python, visita: https://www.python.org/downloads/
    echo.
    goto :end
)

:: Verificar que el script Python existe
if not exist %PYTHON_SCRIPT% (
    echo ERROR: No se encontro el script Python en: %PYTHON_SCRIPT%
    goto :end
)

echo Python detectado:
python --version
echo.
echo Ejecutando benchmark Python...
echo   Input:  %INPUT_DIR%
echo   Output: %OUTPUT_DIR%
echo   Graficos: %GRAFICOS_DIR%
echo.

:: Ejecutar el script Python desde el directorio raiz con las rutas correctas
python %PYTHON_SCRIPT% --input %INPUT_DIR% --output %OUTPUT_DIR% --graficos %GRAFICOS_DIR%

set PYTHON_RESULT=%ERRORLEVEL%

echo.
echo ------------------------------------------------------------

if %PYTHON_RESULT% equ 0 (
    echo Ejecucion Python completada exitosamente
) else (
    echo ERROR durante la ejecucion Python (codigo: %PYTHON_RESULT%)
)

:end
echo.
echo ============================================================
echo   Resumen de ejecucion:
echo     - Java: Compilacion y ejecucion completada
echo     - Python: Ejecucion del benchmark completada
echo ============================================================
echo.
pause
