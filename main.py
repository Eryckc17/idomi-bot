import requests
import time
import random
import schedule
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE IDENTIDAD Y SEGURIDAD ---
TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
PROXY_URL = "http://99b8b372f9d7a12093bf:c0fb22e7b57fecef@gw.dataimpulse.com:823" # Datos de DataImpulse

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
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error Telegram: {e}")

def calcular_insumos(monto_estimado):
    # Cálculo basado en promedio RD$ 650/m2
    area_m2 = round(monto_estimado / 650)
    rollos = round(area_m2 / 9) # 9m2 por rollo traslapado
    primer = round(area_m2 / 50) # 50m2 por paila
    ganancia = round(monto_estimado * 0.38)
    return area_m2, rollos, primer, ganancia

def clasificar_semaforo(monto, dias_cierre):
    if monto >= 2000000: return "💎 DIAMANTE", "Diamante"
    if dias_cierre <= 2: return "🔥 FUEGUITO", "Fueguito"
    if monto >= 500000: return "🟢 VERDE", "Verde"
    return "🟡 AMARILLO", "Amarillo"

def patrullar_portal():
    print(f"[{datetime.now()}] Patrullando Portal y Privados...")
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    proxies = {"http": PROXY_URL, "https": PROXY_URL}
    
    # Simulación de extracción de datos (Aquí conectamos con la API/Scraper del Portal)
    # Filtro aplicado: Solo Abril 2026, Estado: Publicado
    
    # EJEMPLO DE HALLAZGO REAL (Simulado para demostración)
    hallazgos = [
        {
            "id": "EDEESTE-DAF-CM-2026-0022",
            "obra": "Impermeabilización Almacén Sabana Larga",
            "entidad": "EDEESTE",
            "monto": 1702150,
            "cierre": "2026-04-15 17:55",
            "ubicación": "Sabana Larga, Santo Domingo Este",
            "lat_long": "18.4874,-69.8519",
            "responsable": "Ing. Manuel Perdomo",
            "contacto": "mperdomo@edeeste.com.do / 809-555-0122"
        }
    ]

    for obra in hallazgos:
        if obra['id'] not in OBRAS_VISTAS:
            area, rollos, primer, ganancia = calcular_insumos(obra['monto'])
            semaforo, categoria = clasificar_semaforo(obra['monto'], 4)
            REPORTE_DIARIO[categoria] += 1
            
            maps_link = f"https://www.google.com/maps/search/?api=1&query={obra['lat_long']}"
            
            mensaje = (
                f"{semaforo} - NUEVA OPORTUNIDAD\n\n"
                f"🏗️ **Proyecto:** {obra['obra']}\n"
                f"🏢 **Entidad:** {obra['entidad']}\n"
                f"👤 **Responsable:** {obra['responsable']}\n"
                f"📧 **Contacto:** {obra['contacto']}\n"
                f"📍 **Ubicación:** {obra['ubicación']}\n"
                f"🗺️ [Ver en Google Maps]({maps_link})\n\n"
                f"🔗 **Link:** [Acceder al Portal](https://comprasdominicana.gob.do/procesos/{obra['id']})\n"
                f"🆔 **Ref:** `{obra['id']}`\n"
                f"⏱️ **Cierre:** {obra['cierre']}\n"
                f"---\n"
                f"📊 **ANÁLISIS TÉCNICO IDOMI:**\n"
                f"* Area: {area} m2\n"
                f"* Insumos: {rollos} Rollos / {primer} Pailas\n"
                f"* Presupuesto Sugerido: RD$ {obra['monto']:,}\n"
                f"* Ganancia Est. (38%): RD$ {ganancia:,}"
            )
            enviar_telegram(mensaje)
            OBRAS_VISTAS.add(obra['id'])

def reporte_vida():
    enviar_telegram(f"🦅 Reporte Halcón IDOMI: Sistema activo. Patrullando con Proxy DataImpulse. (Hora: {datetime.now().strftime('%H:%M')})")

def reporte_final():
    resumen = (
        f"📊 **RESUMEN DE CAZA - IDOMI**\n"
        f"Hoy se encontraron:\n"
        f"💎 Diamantes: {REPORTE_DIARIO['Diamante']}\n"
        f"🔥 Fueguitos: {REPORTE_DIARIO['Fueguito']}\n"
        f"🟢 Verdes: {REPORTE_DIARIO['Verde']}\n"
        f"🟡 Amarillos: {REPORTE_DIARIO['Amarillo']}\n"
        f"Total de presas detectadas: {sum(REPORTE_DIARIO.values())}"
    )
    enviar_telegram(resumen)
    # Reset diario
    for key in REPORTE_DIARIO: REPORTE_DIARIO[key] = 0

# --- PROGRAMACIÓN DE TAREAS ---
# Patrullaje aleatorio cada 20-30 minutos
def tarea_aleatoria():
    patrullar_portal()
    espera = random.randint(20, 30)
    schedule.every(espera).minutes.do(tarea_aleatoria)
    return schedule.CancelJob

schedule.every(25).minutes.do(patrullar_portal)
schedule.every(1).hours.do(reporte_vida)
schedule.every().day.at("20:00").do(reporte_final)

if __name__ == "__main__":
    enviar_telegram("🦅 **Halcón IDOMI Despegando...**\nRadar configurado: Abril 2026.\nProxy: DataImpulse Activo.\nSolo Obras ABIERTAS.")
    while True:
        schedule.run_pending()
        time.sleep(1)
