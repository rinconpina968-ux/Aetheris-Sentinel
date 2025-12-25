@echo off
:: =================================================================
:: SISTEMA AETHERIS: INSTALADOR Y LANZADOR ÚNICO
:: =================================================================

:: PASO CRÍTICO: Ubica el proceso en la carpeta real de los archivos
:: Esto soluciona el error "No such file or directory"
cd /d "%~dp0"

title AETHERIS SENTINEL - CONFIGURADOR
color 0B
echo ======================================================
echo       CONFIGURACION E INSTALACION DE AETHERIS
echo ======================================================
echo Carpeta detectada: %cd%

:: 1. INSTALACIÓN DE LIBRERÍAS (SUMINISTROS)
echo.
echo [1/3] Instalando piezas de Python...
pip install customtkinter plyer ollama pyttsx3 --quiet
if %errorlevel% neq 0 (
    echo [ERROR] No se pudo instalar Python. Revisa tu conexion.
    pause
    exit
)

:: 2. FABRICACIÓN DEL SENSOR (ENSAMBLAJE)
echo [2/3] Fabricando sensor de hardware (C++)...
if not exist monitor.cpp (
    echo [ERROR] No encuentro monitor.cpp en esta carpeta.
    dir /b
    pause
    exit
)
g++ monitor.cpp -o monitor.exe -lpsapi -liphlpapi
if %errorlevel% neq 0 (
    echo [ERROR] Fallo al compilar el sensor. Revisa g++.
    pause
    exit
)

:: 3. LIMPIEZA Y PREPARACIÓN
echo [3/3] Limpiando reportes viejos...
if exist estado_disco.txt del estado_disco.txt
if exist reporte_red.xml del reporte_red.xml

echo.
echo ======================================================
echo      SISTEMA CONFIGURADO Y LISTO PARA OPERAR
echo ======================================================
echo Presiona una tecla para LANZAR EL DASHBOARD...
pause
python aetheris_gui.py