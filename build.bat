@echo off
chcp 65001 >/dev/null
cls

echo ============================================================
echo   Script de Compilacion - Taller Algoritmos Java + Python
echo ============================================================
echo.

set SRC_DIR=src\java
set BIN_DIR=bin
set MAIN_CLASS=org.algoritmos.Main
set PYTHON_SCRIPT=src\python\main.py
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
javac -d %BIN_DIR% -encoding UTF-8 -sourcepath %SRC_DIR% ^
    %SRC_DIR%\org\algoritmos\util\*.java ^
    %SRC_DIR%\org\algoritmos\ordenamiento\*.java ^
    %SRC_DIR%\org\algoritmos\busqueda\*.java ^
    %SRC_DIR%\org\algoritmos\core\*.java ^
    %SRC_DIR%\org\algoritmos\controller\*.java ^
    %SRC_DIR%\org\algoritmos\Main.java

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

python --version >/dev/null 2>&1
if %ERRORLEVEL% neq 0 (
    echo WARNING: Python no esta instalado o no esta en el PATH
    goto :end
)

if not exist %PYTHON_SCRIPT% (
    echo ERROR: No se encontro el script Python en: %PYTHON_SCRIPT%
    goto :end
)

echo Python detectado:
python --version
echo.
echo Ejecutando benchmark Python...

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
echo   Resumen de ejecucion completado
echo ============================================================
echo.
pause
