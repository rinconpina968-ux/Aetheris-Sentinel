# =================================================================
# AETHERIS SENTINEL v5.4 - PROFESSIONAL EDITION
# =================================================================
import customtkinter as ctk
import subprocess
import os
import xml.etree.ElementTree as ET
import ollama
import pyttsx3
import threading
import psutil

# =================================================================
# NÚCLEO DE SEGURIDAD (KERNEL & SERVICES)
# =================================================================

def aplicar_hardening_permanente(puerto):
    """Bloqueo de Firewall y Servicios de forma segura."""
    try:
        nombre_regla = f"AETHERIS_BLOCK_{puerto}"
        
        # 1. Bloqueo en Firewall vía NETSH (Capa de Hierro)
        subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", f"name={nombre_regla}"], capture_output=True)
        result = subprocess.run([
            "netsh", "advfirewall", "firewall", "add", "rule",
            f"name={nombre_regla}", "dir=in", "action=block", 
            "protocol=TCP", f"localport={puerto}"
        ], capture_output=True)

        # 2. Neutralización de puertos críticos del Sistema (445 / 135)
        servicios_map = {"445": "LanmanServer", "135": "RpcSs", "80": "w3svc"}
        if puerto in servicios_map:
            svc = servicios_map[puerto]
            # Deshabilitar para que no inicie con Windows
            subprocess.run(["sc", "config", svc, "start=disabled"], capture_output=True)
            # Detener el servicio inmediatamente
            subprocess.run(["net", "stop", svc, "/y"], capture_output=True)

        return result.returncode == 0
    except Exception as e:
        return False

# =================================================================
# CLASE PRINCIPAL - INTERFAZ DE SEGURIDAD
# =================================================================

class AetherisSentinel(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AETHERIS SENTINEL v5.4 - Security Core")
        self.geometry("550x750")
        ctk.set_appearance_mode("dark")

        # Asegurar directorio de reportes (C:\ollana)
        self.report_dir = r"C:\ollana"
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

        self.setup_ui()
        
        try:
            self.voice = pyttsx3.init()
            self.voice.setProperty("rate", 180)
        except:
            self.voice = None

    def setup_ui(self):
        self.label_title = ctk.CTkLabel(
            self, text="🛡️ AETHERIS SENTINEL",
            font=("Segoe UI", 24, "bold"), text_color="#00f2ff"
        )
        self.label_title.pack(pady=15)

        self.status_box = ctk.CTkTextbox(
            self, width=500, height=450, font=("Consolas", 11),
            border_color="#1fada8", border_width=1
        )
        self.status_box.pack(pady=10)

        self.btn_run = ctk.CTkButton(
            self, text="INICIAR AUDITORÍA TÉCNICA",
            command=self.iniciar_auditoria, fg_color="#1fada8",
            hover_color="#178a85"
        )
        self.btn_run.pack(pady=10)

        self.defense_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.defense_frame.pack(pady=10)

    def log(self, text, tag="INFO"):
        self.after(0, lambda: self.status_box.insert("end", f"[{tag}] {text}\n"))
        self.after(0, lambda: self.status_box.see("end"))

    def iniciar_auditoria(self):
        self.btn_run.configure(state="disabled", text="ANALIZANDO...")
        self.status_box.delete("0.0", "end")
        threading.Thread(target=self.ejecutar_escaneo, daemon=True).start()

    def ejecutar_escaneo(self):
        self.log("Iniciando escaneo de infraestructura...")
        target = "127.0.0.1"
        xml_path = os.path.join(self.report_dir, "audit_report.xml")

        try:
            # Escaneo con Nmap
            subprocess.run(["nmap", "-F", target, "-oX", xml_path], capture_output=True)

            puertos_encontrados = []
            if os.path.exists(xml_path):
                tree = ET.parse(xml_path)
                for port in tree.findall(".//port"):
                    state = port.find("state")
                    if state is not None and state.get("state") == "open":
                        puertos_encontrados.append(port.get("portid"))

            if puertos_encontrados:
                self.log(f"Puertos abiertos detectados: {puertos_encontrados}", "ALERTA")
                analisis = self.consultar_ia(puertos_encontrados)
                self.log(f"ANÁLISIS IA: {analisis}", "INTEL")
                self.after(0, lambda: self.mostrar_boton_defensa(puertos_encontrados))
            else:
                self.log("No se detectaron servicios expuestos.", "OK")

        except Exception as e:
            self.log(f"Fallo en motor de escaneo: {str(e)}", "CRITICAL")

        self.after(0, lambda: self.btn_run.configure(state="normal", text="INICIAR AUDITORÍA TÉCNICA"))

    def consultar_ia(self, puertos):
        try:
            prompt = f"Analiza estos puertos: {puertos}. Sé técnico, breve y di 'CERRAR' si son peligrosos."
            response = ollama.generate(model="llama3.2", prompt=prompt)
            return response["response"].strip()
        except:
            return "IA Offline. Se sugiere Hardening preventivo."

    def mostrar_boton_defensa(self, puertos):
        for child in self.defense_frame.winfo_children():
            child.destroy()

        btn_fix = ctk.CTkButton(
            self.defense_frame, text="⚡ APLICAR HARDENING PERSISTENTE",
            fg_color="#c0392b", hover_color="#e74c3c",
            command=lambda: threading.Thread(target=self.protocolo_defensa, args=(puertos,), daemon=True).start()
        )
        btn_fix.pack()

    def protocolo_defensa(self, puertos):
        self.log("Ejecutando protocolo de aislamiento...")
        for p in puertos:
            if aplicar_hardening_permanente(p):
                self.log(f"Puerto {p} neutralizado.", "SUCCESS")
            else:
                self.log(f"Error al bloquear puerto {p}.", "WARNING")
        self.log("Hardening finalizado. Sistema protegido.", "SUCCESS")

if __name__ == "__main__":
    app = AetherisSentinel()
    app.mainloop()
