import os
import time
import requests
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB PARA RENDER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "IDOMI VIGILANTE ACTIVO 🚀"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- TUS DATOS ACTUALIZADOS ---
TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
URL_PORTAL = "https://dgcp.gob.do/servicios/consultar-compras-menores/"
PALABRAS_CLAVE = ["lona", "asfaltica", "impermeabilizacion", "techado", "asfalto"]

ultimo_mensaje_id = None

def gestionar_mensajes_estado(mensaje):
    global ultimo_mensaje_id
    base_url = f"https://api.telegram.org/bot{TOKEN}"
    if ultimo_mensaje_id:
        try:
            requests.post(f"{base_url}/deleteMessage", json={"chat_id": CHAT_ID, "message_id": ultimo_mensaje_id}, timeout=5)
        except:
            pass
    try:
        res = requests.post(f"{base_url}/sendMessage", json={"chat_id": CHAT_ID, "text": mensaje}, timeout=10)
        if res.status_code == 200:
            ultimo_mensaje_id = res.json().get("result").get("message_id")
    except:
        pass

def enviar_alerta_real(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje}, timeout=10)
    except:
        pass

def buscar_en_portal():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    hora_ven = time.strftime('%I:%M %p') # Hora formato 12h
    gestionar_mensajes_estado(f"🔍 Revisando portal DGCP...\nÚltima: {hora_ven}\nEstado: EN LÍNEA ✅")
    
    try:
        response = requests.get(URL_PORTAL, headers=headers, timeout=30)
        if response.status_code == 200:
            contenido = response.text.lower()
            for p in PALABRAS_CLAVE:
                if p in contenido:
                    enviar_alerta_real(f"🔔 ¡OPORTUNIDAD DETECTADA!\nPalabra: {p.upper()}\nEntra aquí: {URL_PORTAL}")
                    return
    except:
        print("Error de conexión al portal dominicano")

def bucle_principal():
    print("🚀 Vigilante de IDOMI SRL Iniciado...")
    # Enviamos confirmación de arranque
    enviar_alerta_real("🚀 IDOMI-BOT ACTIVADO\nBuscando lonas cada 20 minutos.")
    
    while True:
        buscar_en_portal()
        time.sleep(1200) # Espera 20 minutos exacta

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle_principal()
