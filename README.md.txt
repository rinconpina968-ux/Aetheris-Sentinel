# 🛡️ Aetheris Sentinel v3.5

> **Sistema integrado de ciberseguridad y monitoreo de hardware con IA local.**

---

## 🏗️ Arquitectura del Proyecto
He diseñado este sistema bajo tres pilares fundamentales que integran diferentes niveles de programación para lograr una solución robusta:

### 🧠 El Cerebro (`aetheris_gui.py`)
* **Lenguaje:** Python
* **Función:** Gestiona la interfaz gráfica (CustomTkinter), procesa logs de sistema y consulta a la IA (**Ollama / Llama 3.2**) para generar diagnósticos de seguridad en lenguaje humano.

### 💪 El Músculo (`monitor.cpp`)
* **Lenguaje:** C++
* **Función:** Sensor de bajo nivel que utiliza las APIs de Windows (`psapi.h`) para medir el uso de RAM y auditar sockets de red en tiempo real (Sistema de Alerta Domo).

### ⚡ El Interruptor (`control_total.bat`)
* **Lenguaje:** Windows Batch
* **Función:** Orquestador del sistema. Automatiza la configuración del entorno, verifica dependencias de Python, compila el código fuente de C++ y lanza la aplicación.

---

## 📊 Capacidades de Análisis
Aetheris no solo muestra datos fríos, sino que realiza una auditoría inteligente:
- **Salud de Hardware:** Monitoreo activo de saturación de memoria RAM.
- **Seguridad de Red:** Detección de conexiones externas activas y escaneo de puertos.
- **Asistente de Voz:** Notificaciones auditivas mediante síntesis de voz para alertas críticas.

---

## 🚀 Cómo empezar

Sigue estos pasos para desplegar el centinela en tu estación de trabajo:

1.  **Requisitos previos:**
    * Tener instalado [Python 3.10+](https://www.python.org/).
    * Un compilador de C++ (como MinGW o MSVC).
    * [Ollama](https://ollama.com/) instalado.

2.  **Configurar la IA:**
    ```bash
    ollama run llama3.2
    ```

3.  **Lanzamiento:**
    * Ejecuta `control_total.bat` con permisos de administrador.
    * Haz clic en **"ANALIZAR SISTEMA"** y espera el diagnóstico de Aetheris.

---
*Desarrollado con un enfoque en eficiencia de hardware, ciberseguridad industrial e inteligencia artificial local.*
