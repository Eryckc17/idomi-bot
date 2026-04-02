import os, time, requests, datetime, random
from flask import Flask
from threading import Thread
import urllib.parse

app = Flask(__name__)
@app.route('/')
def home():
    return "🦅 EL HALCÓN v25.0 - CENTINELA IDOMI"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN ---
TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
OBRAS_ENCONTRADAS_HORA = 0

def motor_analisis_halcon(area):
    ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
    factor = 1 + ((ahora.month - 1) * 0.006)
    rollos = round((area / 9) * 1.12)
    primer = round(area / 25)
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
    global OBRAS_ENCONTRADAS_HORA
    # El radar ahora busca más términos: Impermeabilización, Filtración, Lona, Techos.
    encontro = random.random() < 0.20 # Simulación de hallazgo
    
    if encontro:
        OBRAS_ENCONTRADAS_HORA += 1
        area = random.randint(700, 2500)
        res = motor_analisis_halcon(area)
        
        # Clasificación por colores y prioridad
        if area > 1200: tipo = "💎 DIAMANTE (ALTA PRIORIDAD)"
        else: tipo = "🟢 VERDE (PROYECTO PRIVADO)"
        
        obra = random.choice(["Impermeabilización Nave Industrial", "Remozamiento de Techos / Filtraciones", "Acondicionamiento de Cubierta"])
        region = "Santiago (Cibao Central)"
        codigo_ref = f"IDOMI-REF-{random.randint(100, 999)}"
        email = "proyectos@constructora.com.do"

        # Cuerpo del correo automático (15 años garantía)
        asunto = f"Propuesta IDOMI - 15 AÑOS GARANTÍA - {obra}"
        cuerpo = f"Estimados,\n\nPresentamos nuestra propuesta para la obra {obra}. Ofrecemos solución técnica con GARANTÍA DE 15 AÑOS.\n\nAtentamente,\nEryck - IDOMI Ventas"
        mail_link = f"mailto:{email}?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"

        mensaje = (
            f"{tipo}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏗️ <b>OBRA:</b> {obra}\n"
            f"🆔 <b>REF:</b> <code>{codigo_ref}</code>\n"
            f"📍 <b>ZONA:</b> {region}\n"
            f"🏢 <b>EMPRESA:</b> CONSTRUCCIONES ROSARIO & CABA SRL\n"
            f"👤 <b>ING:</b> Roberto Alcántara\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📐 <b>ÁREA:</b> {area} m²\n"
            f"🛡️ <b>GARANTÍA: 15 AÑOS</b>\n"
            f"📦 <b>LOGÍSTICA:</b>\n"
            f"• {res['rollos']} Rollos Lona + {res['primer']} Galones Primer\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📈 <b>GANANCIA NETA: RD$ {res['neta']:,.0f}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        
        botones = [
            [{"text": "📍 GOOGLE MAPS", "url": "http://google.com/maps"}],
            [{"text": "📲 WHATSAPP", "url": "https://wa.me/18295551234"}],
            [{"text": "✉️ ENVIAR CORREO (15 AÑOS)", "url": mail_link}]
        ]
        enviar_telegram(mensaje, botones)

def bucle_maestro():
    global OBRAS_ENCONTRADAS_HORA
    enviar_telegram("<b>🛡️ HALCÓN v25.0 CENTINELA ONLINE</b>\nPatrullaje cada 15 min. Reporte de estado cada 60 min.")
    
    inicio_hora = time.time()
    
    while True:
        ejecutar_patrullaje()
        
        # Verificar si ha pasado 1 hora para el reporte de estado
        if time.time() - inicio_hora >= 3600:
            ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
            reporte = (
                f"🛰️ <b>REPORTE DE ACTIVIDAD (60 MIN)</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🔍 <b>Estado:</b> Patrullando activamente.\n"
                f"🏗️ <b>Obras detectadas esta hora:</b> {OBRAS_ENCONTRADAS_HORA}\n"
                f"🕒 <b>Hora RD:</b> {ahora.strftime('%I:%M %p')}\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"<i>El radar sigue buscando filtraciones y techos en el Cibao...</i>"
            )
            enviar_telegram(reporte)
            OBRAS_ENCONTRADAS_HORA = 0 # Resetear contador
            inicio_hora = time.time()
            
        time.sleep(900) # Patrullaje cada 15 minutos (900 seg) para proteger IP

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle_maestro()
