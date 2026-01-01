@echo off
:: =================================================================
:: AETHERIS SENTINEL v5.4 - ENTERPRISE INSTALLER & LAUNCHER
:: =================================================================

:: Ubicar proceso en la carpeta real de los archivos
cd /d "%~dp0"
title AETHERIS SENTINEL v5.4 - Security Core
color 0B

:: =================================================================
:: VALIDACIÓN DE PRIVILEGIOS (EL ESCUDO)
:: =================================================================
:: Comprueba si hay permisos de Administrador para poder cerrar puertos 445/135
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] ERROR: Se requieren permisos de ADMINISTRADOR para el Hardening.
    echo Intentando elevar privilegios automáticamente...
    powershell -Command "Start-Process '%0' -Verb RunAs"
    exit /b
)

echo ======================================================
echo       AETHERIS SYSTEM: MODO ADMINISTRADOR ACTIVO
echo ======================================================
echo Carpeta de operacion: %cd%

:: 1. INSTALACIÓN DE LIBRERÍAS (SUMINISTROS)
echo.
echo [1/3] Verificando dependencias de Python...
pip install customtkinter plyer ollama pyttsx3 psutil --quiet
if %errorlevel% neq 0 (
    echo [ERROR] No se pudieron instalar las librerias. Revisa tu conexion.
    pause
    exit
)

:: 2. COMPILACIÓN DEL SENSOR C++ (ENSAMBLAJE)
echo [2/3] Ensamblando sensor de hardware (monitor.exe)...
if exist monitor.cpp (
    g++ monitor.cpp -o monitor.exe -lpsapi -liphlpapi
    if %errorlevel% neq 0 (
        echo [AVISO] Fallo al compilar monitor.cpp. Se usara el binario existente.
    )
) else (
    echo [!] Aviso: monitor.cpp no encontrado, saltando compilacion.
)

:: 3. LIMPIEZA Y PREPARACIÓN
echo [3/3] Limpiando registros temporales...
if exist estado_disco.txt del estado_disco.txt
if exist reporte_red.xml del reporte_red.xml

echo.
echo ======================================================
echo    CONFIGURACION COMPLETA - LISTO PARA OPERAR
echo ======================================================
echo Presiona una tecla para LANZAR EL DASHBOARD...
pause

:: LANZAMIENTO DEL NÚCLEO
python aetheris_gui.py

echo.
echo ======================================================
echo    SESION FINALIZADA - AETHERIS SENTINEL
echo ======================================================
pause
