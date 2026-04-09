@echo off
chcp 65001 >nul

echo ============================================================
echo     Ejecutar Programa - Taller Algoritmos Java
echo ============================================================
echo.

set BIN_DIR=bin
set MAIN_CLASS=org.algoritmos.main.MainCompleto

if not exist %BIN_DIR% (
    echo ERROR: Directorio %BIN_DIR% no encontrado.
    echo Ejecuta build.bat primero para compilar.
    pause
    exit /b 1
)

cd %BIN_DIR%
java %MAIN_CLASS%
cd ..

echo.
pause