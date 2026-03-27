import os
import time
import requests
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB PARA MANTENERLO VIVO ---
app = Flask(__name__) # Corregido para que no salga vacío

@app.route('/')
def home():
    return "IDOMI VIGILANTE ACTIVO 🚀"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN DEL BOT ---
TOKEN = "7864350174:AAH5Z_Yt7_7W78_7W78_7W78_7W78_7W78"
CHAT_ID = "14321007"
URL_PORTAL = "https://dgcp.gob.do/servicios/consultar-compras-menores/"
PALABRAS_CLAVE = ["lona", "asfaltica", "impermeabilizacion", "techado", "asfalto"]

ultimo_mensaje_id = None

def gestionar_mensajes_estado(mensaje):
    global ultimo_mensaje_id
    base_url = f"https://api.telegram.org/bot{TOKEN}"
    if ultimo_mensaje_id:
        try: requests.post(f"{base_url}/deleteMessage", json={"chat_id": CHAT_ID, "message_id": ultimo_mensaje_id}, timeout=5)
        except: pass
    try:
        res = requests.post(f"{base_url}/sendMessage", json={"chat_id": CHAT_ID, "text": mensaje}, timeout=10)
        if res.status_code == 200:
            ultimo_mensaje_id = res.json().get("result").get("message_id")
    except: pass

def enviar_alerta_real(mensaje):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": mensaje}, timeout=10)

def buscar_en_portal():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    hora = time.strftime('%H:%M:%S')
    gestionar_mensajes_estado(f"🔍 Revisando portal...\nÚltima: {hora}\nEstado: FUNCIONANDO ✅")
    
    try:
        response = requests.get(URL_PORTAL, headers=headers, timeout=30)
        if response.status_code == 200:
            contenido = response.text.lower()
            for p in PALABRAS_CLAVE:
                if p in contenido:
                    enviar_alerta_real(f"🔔 ¡OPORTUNIDAD! Palabra: {p.upper()}\nRevisa el portal DGCP.")
                    return
    except: print("Error de conexión al portal")

def bucle_principal():
    print("🚀 Vigilante de IDOMI SRL Iniciado...")
    enviar_alerta_real("🚀 IDOMI-BOT ACTIVADO\nRevisión cada 20 minutos.")
    while True:
        buscar_en_portal()
        time.sleep(1200)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle_principal()
