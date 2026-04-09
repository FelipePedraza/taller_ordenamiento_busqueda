@echo off
chcp 65001 >nul
cls

echo ==========================================
echo   SCRIPT DE LIMPIEZA - TALLER ALGORITMOS
echo ==========================================
echo.

set "BIN_DIR=bin"
set "OUTPUT_DIR=data\output"
set "INPUT_DIR=data\input"

echo [PASO 1] Limpiando archivos compilados...
if exist "%BIN_DIR%" (
    rmdir /s /q "%BIN_DIR%"
    echo    OK: Directorio %BIN_DIR% eliminado
) else (
    echo    INFO: No existe directorio %BIN_DIR%
)
echo.

echo [PASO 2] Gestionando resultados previos...
echo    INFO: Los archivos de resultado se conservan
echo          (se sobrescribiran al ejecutar nuevamente)
echo.

echo [PASO 3] Verificando datos de entrada...
if exist "%INPUT_DIR%" (
    for %%f in ("%INPUT_DIR%\datos_*.txt") do (
        echo    OK: Datos encontrados - %%~nxf
    )
) else (
    echo    INFO: No existen datos de entrada
echo          (se generaran automaticamente al ejecutar)
)
echo.

echo ==========================================
echo   LIMPIEZA COMPLETADA
echo ==========================================
echo.
echo El proyecto esta listo para recompilar.
echo.
echo Proximos pasos:
echo   1. Ejecutar: build.bat
echo   2. O ejecutar: run-ordenamiento.bat
echo   3. O ejecutar: run-busqueda.bat
echo.

pause
