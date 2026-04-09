@echo off
chcp 65001 >nul
cls

echo ============================================================
echo   Script de Compilacion - Taller Algoritmos Java
echo ============================================================
echo.

set SRC_DIR=src\java
set BIN_DIR=bin
set MAIN_CLASS=org.algoritmos.main.MainCompleto

echo [1/4] Limpiando directorio de salida...
if exist %BIN_DIR% (
    rmdir /s /q %BIN_DIR%
)
mkdir %BIN_DIR%
echo     Directorio %BIN_DIR% listo
echo.

echo [2/4] Compilando archivos Java...
javac -d %BIN_DIR% -encoding UTF-8 -sourcepath %SRC_DIR% %SRC_DIR%\org\algoritmos\util\*.java %SRC_DIR%\org\algoritmos\ordenamiento\*.java %SRC_DIR%\org\algoritmos\busqueda\*.java %SRC_DIR%\org\algoritmos\main\*.java

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR de compilacion
    pause
    exit /b 1
)

echo     Compilacion exitosa
echo.

echo [3/4] Verificando compilacion...
set /a count=0
for /r %BIN_DIR% %%f in (*.class) do set /a count+=1
echo     %count% clases compiladas
echo.

echo [4/4] Ejecutando programa...
echo ------------------------------------------------------------

cd %BIN_DIR%
java %MAIN_CLASS%
set RESULT=%ERRORLEVEL%
cd ..

echo ------------------------------------------------------------

if %RESULT% equ 0 (
    echo Ejecucion completada exitosamente
) else (
    echo ERROR durante la ejecucion (codigo: %RESULT%)
)

echo.
pause