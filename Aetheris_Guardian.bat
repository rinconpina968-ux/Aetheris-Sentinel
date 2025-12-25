@echo off
:inicio
:: Ejecuta el monitor de C++
monitor.exe
:: Ejecuta la lógica de Python en modo silencioso
python consultar.py --auto
:: Espera 5 minutos antes del próximo escaneo
timeout /t 300 /nobreak
goto inicio