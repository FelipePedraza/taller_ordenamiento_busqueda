@echo off
chcp 65001 >nul
cls

echo ╔════════════════════════════════════════════════════════════╗
echo ║     Script de Compilación - Taller Algoritmos Java         ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

set SRC_DIR=src\java
set BIN_DIR=bin
set MAIN_CLASS=org.algoritmos.main.MainCompleto

REM Limpiar directorio bin si existe
echo [1/4] Limpiando directorio de salida...
if exist %BIN_DIR% (
    rmdir /s /q %BIN_DIR%
)
mkdir %BIN_DIR%
echo     ✓ Directorio %BIN_DIR% listo
echo.

REM Compilar todas las clases
echo [2/4] Compilando archivos Java...
javac -d %BIN_DIR% -encoding UTF-8 -sourcepath %SRC_DIR% %SRC_DIR%\org\algoritmos\util\*.java %SRC_DIR%\org\algoritmos\ordenamiento\*.java %SRC_DIR%\org\algoritmos\busqueda\*.java %SRC_DIR%\org\algoritmos\main\*.java

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ Error de compilación
    pause
    exit /b 1
)

echo     ✓ Compilación exitosa
echo.

REM Contar clases compiladas
echo [3/4] Verificando compilación...
set /a count=0
for /r %BIN_DIR% %%f in (*.class) do set /a count+=1
echo     ✓ %count% clases compiladas
echo.

REM Ejecutar el programa
echo [4/4] Ejecutando programa...
echo.
echo ════════════════════════════════════════════════════════════
echo.

cd %BIN_DIR%
java %MAIN_CLASS%
set RESULT=%ERRORLEVEL%
cd ..

echo.
echo ════════════════════════════════════════════════════════════
echo.

if %RESULT% equ 0 (
    echo ✓ Ejecución completada exitosamente
    echo.
    echo Archivos generados:
    echo   - data/input/datos_10000.txt
    echo   - data/input/datos_100000.txt
    echo   - data/input/datos_1000000.txt
    echo   - data/output/resultados_java.csv
    echo   - data/output/resultados_java.json
) else (
    echo ❌ Error durante la ejecución (código: %RESULT%)
)

echo.
pause
