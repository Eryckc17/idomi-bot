import os
import time
import requests
from flask import Flask
from threading import Thread

# --- CONFIGURACIÓN DE FLASK PARA RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot de IDOMI SRL Vigilando... 🚀"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- DATOS DE TU BOT ---
TOKEN = "7864350174:AAH5Z_Yt7_7W78_7W78_7W78_7W78_7W78"
CHAT_ID = "14321007"
URL_PORTAL = "https://dgcp.gob.do/servicios/consultar-compras-menores/"

PALABRAS_CLAVE = ["lona", "asfaltica", "impermeabilizacion", "techado", "asfalto"]

# Variable global para guardar el ID del último mensaje de "Buscando"
ultimo_mensaje_id = None

def gestionar_mensajes_estado(mensaje):
    global ultimo_mensaje_id
    base_url = f"https://api.telegram.org/bot{TOKEN}"
    
    # 1. Intentar borrar el mensaje anterior si existe
    if ultimo_mensaje_id:
        try:
            requests.post(f"{base_url}/deleteMessage", json={"chat_id": CHAT_ID, "message_id": ultimo_mensaje_id}, timeout=5)
        except:
            pass # Si no puede borrarlo (ej. pasaron más de 48h), sigue adelante

    # 2. Enviar el nuevo mensaje de estado
    try:
        res = requests.post(f"{base_url}/sendMessage", json={"chat_id": CHAT_ID, "text": mensaje}, timeout=10)
        if res.status_code == 200:
            ultimo_mensaje_id = res.json().get("result").get("message_id")
    except Exception as e:
        print(f"Error enviando a Telegram: {e}")

def enviar_alerta_real(mensaje):
    # Este se usa para las alertas de lona (estos NO se borran)
    url_tel = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url_tel, json={"chat_id": CHAT_ID, "text": mensaje}, timeout=10)
    except:
        pass

def buscar_en_portal():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9"
    }
    
    hora_actual = time.strftime('%H:%M:%S')
    gestionar_mensajes_estado(f"🔍 Buscando oportunidades...\nÚltima revisión: {hora_actual}\nEstado: EN LÍNEA ✅")

    intentos = 3
    for i in range(intentos):
        try:
            response = requests.get(URL_PORTAL, headers=headers, timeout=30)
            if response.status_code == 200:
                contenido = response.text.lower()
                for palabra in PALABRAS_CLAVE:
                    if palabra in contenido:
                        enviar_alerta_real(f"🔔 ¡ALERTA IDOMI! Se encontró: {palabra.upper()}\nFecha: {time.strftime('%d/%m/%Y')}\nRevisa el portal ahora.")
                        return 
                return 
        except:
            time.sleep(10)

def bucle_principal():
    print("🚀 Vigilante de IDOMI SRL Iniciado...")
    enviar_alerta_real("🚀 IDOMI-BOT ACTIVADO\nRevisión automática cada 20 minutos.")
    
    while True:
        buscar_en_portal()
        # Espera 20 minutos (1200 segundos)
        time.sleep(1200) 

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    bucle_principal()
