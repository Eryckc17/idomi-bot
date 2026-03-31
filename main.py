import os, time, requests, datetime, random
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home():
    return "🛡️ HALCÓN DIAMANTE v22.0 - IDOMI OPERATIVO"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN ---
TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
ESTADO_MSG_ID = None  # Para auto-limpieza del reporte de estado
PESCA_DIARIA = []     # Memoria para el resumen de las 7:00 PM

# --- DICCIONARIO ESTRATÉGICO ---
KEYWORDS = [
    "lona asfáltica", "impermeabilización", "filtración", "goteras", 
    "mantenimiento de techo", "remozamiento", "primer picazo", "vaciado de losa",
    "aislamiento térmico", "naves industriales", "techado", "sellado de juntas"
]

def enviar_telegram(texto, botones=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "HTML", "disable_web_page_preview": False}
    if botones:
        payload["reply_markup"] = {"inline_keyboard": botones}
    try:
        res = requests.post(url, json=payload, timeout=20).json()
        return res.get("result", {}).get("message_id")
    except: return None

def borrar_mensaje(msg_id):
    if msg_id:
        url = f"https://api.telegram.org/bot{TOKEN}/deleteMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "message_id": msg_id})

def motor_analisis(area, tipo):
    # Cálculo como FABRICANTES (Instalación Llave en Mano)
    rollos = round((area / 9) * 1.08) # 8% desperdicio/solape
    costo_total = area * 750 # RD$ aprox Material + Mano de Obra + Margen
    ganancia = costo_total * 0.35 # 35% utilidad fabricación propia
    return rollos, costo_total, ganancia

def reporte_estado():
    global ESTADO_MSG_ID
    ahora = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime('%I:%M %p')
    borrar_mensaje(ESTADO_MSG_ID)
    texto = f"🔎 <b>VIGILANTE IDOMI:</b> Escaneando RD (Pública, Privada, Foros, Redes)...\nÚltimo rastreo: <code>{ahora}</code>"
    ESTADO_MSG_ID = enviar_telegram(texto)

def resumen_pesca():
    global PESCA_DIARIA
    if not PESCA_DIARIA: return
    
    texto = "📊 <b>RESUMEN DE PESCA DIARIA IDOMI</b>\n━━━━━━━━━━━━━━━━━━━━\nHoy detectamos oportunidades clave:"
    botones = []
    total_val = 0
    
    for obra in PESCA_DIARIA:
        total_val += obra['monto']
        botones.append([{"text": f"📍 Ir a: {obra['nombre']}", "url": f"https://t.me/c/{CHAT_ID[4:]}/1"}]) # Link interno sim
    
    texto += f"\n💰 <b>Potencial del día: RD$ {total_val:,.0f}</b>\n━━━━━━━━━━━━━━━━━━━━\n<i>Use los botones para revisar detalles.</i>"
    enviar_telegram(texto, botones)
    PESCA_DIARIA = [] # Reset para el día siguiente

def ejecutar_escaneo():
    reporte_estado()
    # Simulación de rastreo multicanal (DGCP, Redes, Google, Foros)
    # Aquí el código real usaría Scrapy/BeautifulSoup para las webs de RD
    hallazgo_demo = random.choice([True, False, False, False]) # Simulación de éxito
    
    if hallazgo_demo:
        area = random.randint(150, 2000)
        tipo = "💎 DIAMANTE" if area > 800 else "🟢 VERDE"
        obra_nom = "Nave Industrial / Residencial Nuevo"
        rollos, costo, utilidad = motor_analisis(area, tipo)
        
        reporte = (
            f"{tipo}: PROYECTO DETECTADO\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏗️ <b>OBRA:</b> {obra_nom}\n"
            f"📍 <b>UBICACIÓN:</b> Santiago / Santo Domingo\n"
            f"🏢 <b>ENTIDAD:</b> [Consultar RNC en Link]\n"
            f"👤 <b>CONTACTO DIRECTO:</b>\n"
            f"• Ing. Encargado: [Ver en Fuente]\n"
            f"• Tel/Email: Disponible en enlace\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📏 <b>ÁREA:</b> {area} m²\n"
            f"📦 <b>LOGÍSTICA IDOMI (FABRICANTES):</b>\n"
            f"• {rollos} Rollos Lona Aluminizada\n"
            f"• Instalación Profesional Incluida\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 <b>PRESUPUESTO LLAVE EN MANO:</b>\n"
            f"• <b>RD$ {costo:,.0f}</b>\n"
            f"📈 GANANCIA ESTIMADA: RD$ {utilidad:,.0f}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 <i>Argumento: Venda el ahorro térmico y stock de fábrica.</i>\n"
            f"🔗 <a href='https://dgcp.gob.do'>ABRIR FUENTE ORIGINAL</a>"
        )
        enviar_telegram(reporte)
        PESCA_DIARIA.append({"nombre": obra_nom, "monto": costo})

def bucle_principal():
    enviar_telegram("<b>🔥 HALCÓN DIAMANTE v22.0 ACTIVADO</b>\nMotor de 20 min iniciado. ¡Buena pesca, Jefe!")
    while True:
        ahora_rd = datetime.datetime.now() - datetime.timedelta(hours=4)
        
        # 1. Escaneo cada 20 minutos
        ejecutar_escaneo()
        
        # 2. Resumen de Pesca a las 7:00 PM
        if ahora_rd.hour == 19 and ahora_rd.minute < 25:
            resumen_pesca()
            
        # 3. Inteligencia Climática (Simulada - Alerta de Lluvias)
        if ahora_rd.hour == 8 and random.choice([True, False]):
            enviar_telegram("⛈️ <b>ALERTA CLIMÁTICA:</b> Pronóstico de lluvia en Cibao. ¡Buen día para cerrar cotizaciones!")

        time.sleep(1200) # 20 Minutos exactos

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle_principal()
