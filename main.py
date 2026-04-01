import os, time, requests, datetime, random
from flask import Flask
from threading import Thread
import urllib.parse

app = Flask(__name__)
@app.route('/')
def home():
    return "🦅 EL HALCÓN v24.9 - MAESTRÍA IDOMI"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN ---
TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"

def motor_analisis_halcon(area):
    ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
    factor = 1 + ((ahora.month - 1) * 0.006)
    rollos = round((area / 9) * 1.12)
    primer = round(area / 25) # Cálculo de galones recuperado
    costo_mat = (rollos * 2950 * factor) + (primer * 1100 * factor)
    costo_mo_log = (area * 280 * factor) + 12000
    precio_sugerido = area * 1050
    ganancia = precio_sugerido - (costo_mat + costo_mo_log)
    return {"rollos": rollos, "primer": primer, "costo": costo_mat + costo_mo_log, "total": precio_sugerido, "neta": ganancia}

def enviar_telegram(texto, botones=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "HTML", "disable_web_page_preview": True}
    if botones: payload["reply_markup"] = {"inline_keyboard": botones}
    try:
        requests.post(url, json=payload, timeout=20)
    except: pass

def ejecutar_patrullaje():
    if random.random() < 0.25:
        area = random.randint(700, 2200)
        res = motor_analisis_halcon(area)
        
        # Lógica de Colores y Estados
        if area > 1200:
            tipo = "💎 DIAMANTE (ALTA PRIORIDAD)"
        else:
            tipo = "🟢 VERDE (PROYECTO PRIVADO)"
            
        # Simulación de Licitación Pública
        es_publico = random.choice([True, False])
        estado_extra = ""
        if es_publico:
            tipo = "🟡 AMARILLO (OBRA PÚBLICA)"
            ofertas = random.randint(0, 5)
            estado_extra = f"\n📢 <b>ESTADO:</b> PUBLICADO\n👥 <b>OFERTAS:</b> {ofertas} recibidas (¡Puedes contraofertar!)"

        codigo_ref = f"IDOMI-REF-{random.randint(100, 999)}"
        empresa = "CONSTRUCCIONES ROSARIO & CABA SRL"
        email = "proyectos@rosariocaba.com.do"
        obra = "Impermeabilización Edificación / Nave"
        region = "Santiago (Cibao Central)"

        # Estructura de Correo Automático
        asunto = f"Propuesta Técnica IDOMI - 15 AÑOS GARANTÍA - {obra}"
        cuerpo = f"Estimados de {empresa},\n\nPresentamos propuesta para la obra en {region}. Ofrecemos solución técnica con GARANTÍA DE 15 AÑOS certificada.\n\nContamos con equipo listo para medición inmediata.\n\nAtentamente,\nEryck - IDOMI Ventas"
        mail_link = f"mailto:{email}?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"

        alerta = (
            f"{tipo}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏗️ <b>OBRA:</b> {obra}\n"
            f"🆔 <b>REF:</b> <code>{codigo_ref}</code>{estado_extra}\n"
            f"📍 <b>ZONA:</b> {region}\n"
            f"🏢 <b>EMPRESA:</b> {empresa}\n"
            f"👤 <b>ING:</b> Roberto Alcántara\n"
            f"📞 <b>TEL:</b> 8295551234\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📐 <b>ÁREA:</b> {area} m²\n"
            f"🛡️ <b>GARANTÍA: 15 AÑOS</b>\n"
            f"📦 <b>LOGÍSTICA:</b>\n"
            f"• {res['rollos']} Rollos Lona + {res['primer']} Galones Primer\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 <b>NEGOCIO:</b>\n"
            f"• Inversión: RD$ {res['costo']:,.0f}\n"
            f"💵 <b>PRECIO SUGERIDO: RD$ {res['total']:,.0f}</b>\n"
            f"📈 <b>GANANCIA NETA: RD$ {res['neta']:,.0f}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )

        # BOTONES TIPO CLICK (INTERACTIVOS)
        botones = [
            [{"text": "📍 VER EN GOOGLE MAPS", "url": "https://maps.google.com"}],
            [{"text": "📲 CONTACTAR WHATSAPP", "url": "https://wa.me/18295551234"}],
            [{"text": "✉️ ENVIAR CORREO (15 AÑOS)", "url": mail_link}]
        ]
        enviar_telegram(alerta, botones)

def bucle():
    enviar_telegram("<b>🦅 EL HALCÓN v24.9 ONLINE</b>\nClasificación por colores y logística completa activada.")
    while True:
        ejecutar_patrullaje()
        time.sleep(1200)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle()
    
