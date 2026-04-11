import os
import requests
import time
import random
import schedule
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# --- 1. CORAZÓN PARA MANTENERLO VIVO EN RENDER (GRATIS) ---
app = Flask('')

@app.route('/')
def home():
    return "Halcón IDOMI está patrullando en segundo plano..."

def run():
    # Render busca el puerto 8080. Con esto el bot nunca se apaga.
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. CONFIGURACIÓN DE SEGURIDAD (VARIABLES DE ENTORNO) ---
# En Render, ve a 'Environment' y agrega: TELEGRAM_TOKEN, TELEGRAM_CHAT_ID y PROXY_URL
TOKEN = os.getenv("TELEGRAM_TOKEN", "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "644581238")
PROXY_URL = os.getenv("PROXY_URL", "http://99b8b372f9d7a12093bf:c0fb22e7b57fecef@gw.dataimpulse.com:823")

# Rotación de Navegadores
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
]

# --- 3. LÓGICA DE NEGOCIO IDOMI ---
KEYWORDS = ["impermeabilizacion", "lona asfaltica", "manto asfaltico", "aluminizada", "techo", "filtracion"]
OBRAS_VISTAS = set()
REPORTE_DIARIO = {"Diamante": 0, "Fueguito": 0, "Naranja": 0, "Verde": 0, "Amarillo": 0}

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": mensaje, 
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        requests.post(url, json=payload, timeout=15)
    except Exception as e:
        print(f"Error Telegram: {e}")

def calcular_insumos(monto_estimado):
    area_m2 = round(monto_estimado / 650)
    rollos = round(area_m2 / 9)
    primer = round(area_m2 / 50)
    ganancia = round(monto_estimado * 0.38)
    return area_m2, rollos, primer, ganancia

def clasificar_semaforo(monto, dias_cierre):
    if monto >= 2000000: return "💎 DIAMANTE", "Diamante"
    if dias_cierre <= 2: return "🔥 FUEGUITO", "Fueguito"
    if monto >= 500000: return "🟢 VERDE", "Verde"
    return "🟡 AMARILLO", "Amarillo"

def patrullar_portal():
    print(f"[{datetime.now()}] Iniciando Patrullaje con Proxy DataImpulse...")
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    proxies = {"http": PROXY_URL, "https": PROXY_URL}
    
    # Aquí es donde se conectará con el portal
    hallazgos = [] 

    for obra in hallazgos:
        if obra['id'] not in OBRAS_VISTAS:
            area, rollos, primer, ganancia = calcular_insumos(float(obra['monto']))
            fecha_fin = datetime.strptime(obra['cierre'], "%Y-%m-%d %H:%M")
            dias_restantes = (fecha_fin - datetime.now()).days
            
            semaforo, categoria = clasificar_semaforo(float(obra['monto']), dias_restantes)
            REPORTE_DIARIO[categoria] += 1
            
            maps_link = f"https://www.google.com/maps/search/?api=1&query={obra['ubicación'].replace(' ', '+')}"
            
            mensaje = (
                f"{semaforo} - NUEVA OPORTUNIDAD ABIERTA\n\n"
                f"🏗️ **Proyecto:** {obra['obra']}\n"
                f"🏢 **Entidad:** {obra['entidad']}\n"
                f"👤 **Responsable:** {obra['responsable']}\n"
                f"📧 **Contacto:** {obra['contacto']}\n"
                f"📍 **Ubicación:** {obra['ubicación']}\n"
                f"🗺️ [Ver en Google Maps]({maps_link})\n\n"
                f"🔗 **Link Portal:** [Click para Cotizar](https://comprasdominicana.gob.do/procesos/{obra['id']})\n"
                f"🆔 **Ref:** `{obra['id']}`\n"
                f"⏱️ **Cierre:** {obra['cierre']}\n"
                f"---\n"
                f"📊 **ANÁLISIS TÉCNICO IDOMI:**\n"
                f"* Área estimada: {area:,} m²\n"
                f"* Insumos: {rollos} Rollos / {primer} Pailas\n"
                f"* Presupuesto Sugerido: RD$ {obra['monto']:,}\n"
                f"* Ganancia Est. (38%): RD$ {ganancia:,}"
            )
            enviar_telegram(mensaje)
            OBRAS_VISTAS.add(obra['id'])

def reporte_vida():
    enviar_telegram(f"🦅 **Halcón IDOMI Activo**\nPatrullando... Todo bajo control.")

def reporte_final():
    resumen = (
        f"📊 **RESUMEN DE CAZA DIARIA - IDOMI**\n\n"
        f"💎 Diamantes: {REPORTE_DIARIO['Diamante']}\n"
        f"🔥 Fueguitos: {REPORTE_DIARIO['Fueguito']}\n"
        f"🟢 Verdes: {REPORTE_DIARIO['Verde']}\n"
        f"🟡 Amarillos: {REPORTE_DIARIO['Amarillo']}\n\n"
        f"Total de presas hoy: {sum(REPORTE_DIARIO.values())}"
    )
    enviar_telegram(resumen)
    for key in REPORTE_DIARIO: REPORTE_DIARIO[key] = 0

# --- PROGRAMACIÓN DE TAREAS ---
schedule.every(25).minutes.do(patrullar_portal)
schedule.every(1).hours.do(reporte_vida)
schedule.every().day.at("20:00").do(reporte_final)

if __name__ == "__main__":
    # Arrancamos el servidor falso para Render
    keep_alive()
    
    enviar_telegram("🦅 **Mega-Bot IDOMI Online**\nVersión 2.0 (Seguridad y Estabilidad)")
    
    while True:
        schedule.run_pending()
        time.sleep(1)
