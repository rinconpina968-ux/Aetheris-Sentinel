import customtkinter as ctk
import subprocess
import os
import logging
import xml.etree.ElementTree as ET
from plyer import notification
import ollama
import pyttsx3
import threading  # Para que la voz no congele la ventana

# =================================================================
# BLOQUE 0: CONFIGURACIÓN GENERAL Y LOGS
# =================================================================
# Configuración del archivo de auditoría (La Caja Negra)
logging.basicConfig(
    filename="aetheris_history.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Inicialización del motor de voz (Text-to-Speech)
try:
    engine = pyttsx3.init()
    # Configuración opcional: velocidad y volumen
    engine.setProperty("rate", 150)
except Exception as e:
    logging.error(f"Error iniciando motor de voz: {e}")


# =================================================================
# BLOQUE 1: CEREBRO IA (Ollama + Voz)
# =================================================================
def hablar_en_hilo(texto):
    """
    Ejecuta la voz en un subproceso para no congelar la interfaz gráfica.
    """

    def _speak():
        try:
            engine.say(texto)
            engine.runAndWait()
        except:
            pass

    threading.Thread(target=_speak).start()


def obtener_consejo_ia(datos_hw, datos_red):
    """
    Envía los reportes técnicos a Llama 3.2 para obtener un resumen ejecutivo.
    """
    print("--- ENVIANDO DATOS A OLLAMA ---")  # Debug en consola
    prompt = f"""
    Eres Aetheris, un experto en ciberseguridad.
    Analiza estos datos técnicos y dame un consejo de seguridad MUY BREVE (máximo 20 palabras).
    Sé directo y autoritario.

    [ESTADO DEL PC]:
    {datos_hw}

    [ESTADO DE LA RED]:
    {datos_red}

    Si todo parece bien, di "Sistemas nominales".
    """

    try:
        # Llamada a la API local de Ollama
        response = ollama.generate(model="llama3.2", prompt=prompt)
        return response["response"]
    except Exception as e:
        error_msg = f"Error conectando con IA: Verifica que Ollama esté corriendo."
        logging.error(error_msg)
        return error_msg


# =================================================================
# BLOQUE 2: VISIÓN DE RED (NMAP PARSER)
# =================================================================
def analizar_nmap(archivo_xml):
    """
    Convierte el XML técnico de Nmap en texto legible para humanos y para la IA.
    """
    if not os.path.exists(archivo_xml):
        return "No se ha realizado escaneo de red (Falta reporte XML)."

    try:
        tree = ET.parse(archivo_xml)
        root = tree.getroot()
        hallazgos = []

        # Buscamos hosts y puertos abiertos
        for host in root.findall("host"):
            ip = host.find("address").get("addr")
            for port in host.findall(".//port"):
                port_id = port.get("portid")
                state = port.find("state").get("state")
                if state == "open":
                    hallazgos.append(f"Puerto {port_id} ABIERTO en {ip}")

        if hallazgos:
            resumen = " | ".join(hallazgos)
            return f"ALERTA: {resumen}"
        return "RED SEGURA: No se detectaron puertos vulnerables."

    except Exception as e:
        return f"Error leyendo reporte Nmap: {e}"


# =================================================================
# BLOQUE 3: INTERFAZ GRÁFICA (CUERPO PRINCIPAL)
# =================================================================
class AetherisSentinel(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configuración de la Ventana ---
        self.title("AETHERIS SENTINEL v3.5 - IA INTEGRADA")
        self.geometry("500x700")
        ctk.set_appearance_mode("dark")

        # --- Elementos Visuales (Widgets) ---
        self.label = ctk.CTkLabel(
            self,
            text="CENTRO DE MANDO AETHERIS",
            font=("Roboto", 22, "bold"),
            text_color="#1fada8",
        )
        self.label.pack(pady=20)

        # Indicador de RAM
        self.ram_label = ctk.CTkLabel(
            self, text="RAM: En espera...", font=("Roboto", 18)
        )
        self.ram_label.pack(pady=10)

        # Pantalla de Resultados (Log en pantalla)
        self.status_box = ctk.CTkTextbox(
            self, width=450, height=350, font=("Consolas", 12), border_width=2
        )
        self.status_box.pack(pady=10, padx=20)

        # Botón de Acción
        self.btn_run = ctk.CTkButton(
            self,
            text="ANALIZAR SISTEMA CON IA",
            fg_color="#1fada8",
            hover_color="#14827d",
            font=("Roboto", 14, "bold"),
            height=40,
            command=self.ejecutar_prueba,  # Conecta con la función maestra
        )
        self.btn_run.pack(pady=20)

    def enviar_notificacion(self, titulo, msg):
        """Muestra una alerta nativa de Windows"""
        try:
            notification.notify(
                title=titulo, message=msg, app_name="Aetheris", timeout=5
            )
        except:
            pass  # Ignoramos errores de notificación si fallan

    def ejecutar_prueba(self):
        """
        ORQUESTADOR DE PROCESOS:
        1. Ejecuta C++ (Sensor)
        2. Lee Archivos (Monitor + Nmap)
        3. Consulta a la IA (Ollama)
        4. Actualiza la pantalla y Habla
        """
        # Paso 1: Feedback visual inmediato
        self.status_box.delete("0.0", "end")
        self.status_box.insert("end", "> Iniciando sensores...\n")
        self.update()  # Fuerza a la ventana a actualizarse

        # Paso 2: Ejecutar el sensor de bajo nivel (monitor.exe)
        if os.path.exists("monitor.exe"):
            subprocess.run(["monitor.exe"], shell=True)
        else:
            self.status_box.insert("end", "[ERROR] No se encuentra monitor.exe\n")

        # Paso 3: Recopilar Datos (Hardware + Red)
        datos_hw = "Sin datos de hardware."
        if os.path.exists("estado_disco.txt"):
            with open("estado_disco.txt", "r") as f:
                datos_hw = f.read()

        datos_red = analizar_nmap("reporte_red.xml")

        # Mostrar datos crudos en pantalla
        self.status_box.insert("end", f"--- HARDWARE ---\n{datos_hw}\n")
        self.status_box.insert("end", f"--- RED ---\n{datos_red}\n")

        # Actualizar etiqueta de RAM visualmente
        try:
            if "RAM Usage:" in datos_hw:
                ram_val = datos_hw.split("RAM Usage:")[1].split("%")[0].strip()
                self.ram_label.configure(text=f"RAM: {ram_val}%")
        except:
            pass

        # Paso 4: CONSULTA A LA INTELIGENCIA ARTIFICIAL
        self.status_box.insert("end", "\n> Analizando con Llama 3.2 (Pensando...)\n")
        self.update()

        # Obtenemos el consejo
        consejo = obtener_consejo_ia(datos_hw, datos_red)

        # Paso 5: Resultado Final
        self.status_box.insert("end", f"\n[IA DICE]: {consejo}\n")
        self.status_box.see("end")  # Auto-scroll al final

        # Alertas Humanas (Voz y Notificación)
        hablar_en_hilo(consejo)
        self.enviar_notificacion("Consejo de Aetheris", consejo)

        logging.info("Ciclo de auditoría completado con éxito.")


# =================================================================
# INICIO DE PRODUCCIÓN
# =================================================================
if __name__ == "__main__":
    app = AetherisSentinel()
    app.mainloop()
