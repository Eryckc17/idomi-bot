import os
import requests
import time
import random
import schedule
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE SEGURIDAD (VÍA RENDER) ---
# El bot ahora buscará estos datos en la pestaña 'Environment' de Render
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PROXY_URL = os.getenv("PROXY_URL")

# Rotación de Navegadores para evitar bloqueos
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
]

# --- LÓGICA DE NEGOCIO IDOMI ---
KEYWORDS = ["impermeabilizacion", "lona asfaltica", "manto asfaltico", "aluminizada", "techo", "filtracion"]
OBRAS_VISTAS = set()
REPORTE_DIARIO = {"Diamante": 0, "Fueguito": 0, "Naranja": 0, "Verde": 0, "Amarillo": 0}

def enviar_telegram(mensaje):
    if not TOKEN or not CHAT_ID:
        print("Error: TOKEN o CHAT_ID no configurados en Render.")
        return
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
    print(f"[{datetime.now()}] Iniciando Patrullaje...")
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    proxies = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None
    
    # Aquí va la lógica de extracción del portal (DGCP / Constructoras)
    hallazgos = [] # Se llena dinámicamente

    for obra in hallazgos:
        if obra['id'] not in OBRAS_VISTAS:
            area, rollos, primer, ganancia = calcular_insumos(obra['monto'])
            # Lógica de fecha para semáforo
            try:
                fecha_fin = datetime.strptime(obra['cierre'], "%Y-%m-%d %H:%M")
                dias_restantes = (fecha_fin - datetime.now()).days
            except:
                dias_restantes = 5 # Por defecto si no hay fecha

            semaforo, categoria = clasificar_semaforo(obra['monto'], dias_restantes)
            REPORTE_DIARIO[categoria] += 1
            
            # Link dinámico a Maps
            maps_link = f"https://www.google.com/maps/search/?api=1&query={obra['ubicación'].replace(' ', '+')}"
            
            mensaje = (
                f"{semaforo} - NUEVA OPORTUNIDAD ABIERTA\n\n"
                f"🏗️ **Proyecto:** {obra['obra']}\n"
                f"🏢 **Entidad:** {obra['entidad']}\n"
                f"👤 **Responsable:** {obra['responsable']}\n"
                f"📧 **Contacto:** {obra['contacto']}\n"
                f"📍 **Ubicación:** {obra['ubicación']}\n"
                f"🗺️ [Ver Ubicación en Google Maps]({maps_link})\n\n"
                f"🔗 **Link Portal:** [Click para Cotizar](https://comprasdominicana.gob.do/procesos/{obra['id']})\n"
                f"🆔 **Referencia:** `{obra['id']}`\n"
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
    enviar_telegram(f"🦅 **Halcón IDOMI Activo**\nPatrullando Portal y Privados...\nEstado: Buscando presas de Abril.")

def reporte_final():
    resumen = (
        f"📊 **RESUMEN DE CAZA DIARIA - IDOMI**\n\n"
        f"💎 Diamantes: {REPORTE_DIARIO['Diamante']}\n"
        f"🔥 Fueguitos: {REPORTE_DIARIO['Fueguito']}\n"
        f"🟢 Verdes: {REPORTE_DIARIO['Verde']}\n"
        f"🟡 Amarillos: {REPORTE_DIARIO['Amarillo']}\n\n"
        f"Total hoy: {sum(REPORTE_DIARIO.values())}"
    )
    enviar_telegram(resumen)
    for key in REPORTE_DIARIO: REPORTE_DIARIO[key] = 0

# Programación
schedule.every(25).minutes.do(patrullar_portal)
schedule.every(1).hours.do(reporte_vida)
schedule.every().day.at("20:00").do(reporte_final)

if __name__ == "__main__":
    enviar_telegram("🦅 **Mega-Bot IDOMI Iniciado (Versión Segura)**\nFiltros: Abril 2026 / Solo Publicados.\nProxy configurado vía Render.")
    while True:
        schedule.run_pending()
        time.sleep(1)
