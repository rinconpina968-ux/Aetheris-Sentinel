# 🛡️ Aetheris Sentinel v3.5

Sistema integrado de ciberseguridad y monitoreo de hardware con IA local.

## 🏗️ Arquitectura del Proyecto
He diseñado este sistema bajo tres pilares fundamentales que integran diferentes niveles de programación:

* **🧠 El Cerebro (`aetheris_gui.py`):** Desarrollado en **Python**.
       Gestiona la interfaz gráfica (CustomTkinter), procesa los logs y consulta a la IA (**Ollama / Llama 3.2**)
       para generar diagnósticos de seguridad en lenguaje humano.
* **💪 El Músculo (`monitor.cpp`):** Desarrollado en **C++**. Un sensor de bajo nivel que utiliza las APIs 
      de Windows para medir el uso de RAM y auditar sockets de red en tiempo real (Sistema de Alerta Domo).
* **⚡ El Interruptor (`control_total.bat`):** El orquestador del sistema. Automatiza la configuración del entorno,
      descarga dependencias, compila el código fuente de C++ y lanza la aplicación.

## 📊 Capacidades de Análisis
Aetheris no solo muestra datos, sino que analiza:
- **Salud de Hardware:** Monitoreo de saturación de memoria RAM.
- **Seguridad de Red:** Detección de conexiones externas activas y escaneo de puertos mediante integración con Nmap.
- **Asistente de Voz:** Notificaciones auditivas de riesgos detectados.

## 🚀 Cómo empezar
1. **Requisitos:** Tener instalado Python 3.10+, un compilador de C++ (g++) y [Ollama](https://ollama.com/).
2. **Modelo IA:** Descarga el cerebro ejecutando `ollama run llama3.2` en tu terminal.
3. **Arranque:** Ejecuta `control_total.bat` con permisos de administrador.
4. **Operación:** Pulsa "ANALIZAR SISTEMA" y escucha el diagnóstico de la IA.

---
*Proyecto desarrollado con enfoque en eficiencia de hardware, ciberseguridad industrial e inteligencia artificial local.*