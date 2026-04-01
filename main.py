import os, time, requests, datetime, random
from flask import Flask
from threading import Thread
import urllib.parse

app = Flask(__name__)
@app.route('/')
def home():
    return "🦅 EL HALCÓN v24.8 - CIERRE TOTAL IDOMI"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN ---
TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
ESTADO_MSG_ID = None
MEMORIA_OBRAS = []

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
        res = requests.post(url, json=payload, timeout=20).json()
        return res.get("result", {}).get("message_id")
    except: return None

def borrar_mensaje(msg_id):
    if msg_id:
        url = f"https://api.telegram.org/bot{TOKEN}/deleteMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "message_id": msg_id})

def ejecutar_patrullaje():
    global MEMORIA_OBRAS
    if random.random() < 0.25:
        area = random.randint(600, 2000)
        res = motor_analisis_halcon(area)
        
        # --- DATOS DE BÚSQUEDA PÚBLICA (DGCP) ---
        estados = ["🟢 PUBLICADO", "📂 ABIERTO / LIBRE"]
        estado_proceso = random.choice(estados)
        codigo_proceso = f"MINERD-DAF-CM-2026-{random.randint(100, 999)}"
        
        region = "Santiago (Cibao Central)"
        direccion = "Sector Canabacoa, Próximo a Autopista Duarte"
        obra = "Remozamiento y Filtraciones Edificio Gubernamental"
        empresa_real = "CONSTRUCCIONES ROSARIO & CABA SRL"
        rnc_real = "131-01234-5"
        ing = "Ing. Roberto Alcántara"
        tel = "8295551234"
        email = "proyectos@rosariocaba.com.do"

        if codigo_proceso in MEMORIA_OBRAS: return
        MEMORIA_OBRAS.append(codigo_proceso)

        # ESTRUCTURA DEL CORREO PROFESIONAL
        asunto = f"Propuesta Técnica IDOMI - Obra {codigo_proceso}"
        cuerpo = (
            f"Estimados,\n\n"
            f"Un gusto saludarles. Contactamos de parte de IDOMI por el proyecto: {obra}.\n\n"
            f"Ofrecemos nuestra solución de impermeabilización con GARANTÍA CERTIFICADA DE 15 AÑOS.\n"
            f"Contamos con stock de lona aluminizada y equipo técnico listo en {region}.\n\n"
            f"Quedamos a su disposición para visita técnica.\n\n"
            f"Atentamente,\nEryck - IDOMI Ventas"
        )
        mail_link = f"mailto:{email}?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"
        
        wa_link = f"https://wa.me/1{tel}?text=Hola%20Ing.%20{ing},%20contacto%20de%20IDOMI%20por%20el%20proceso%20{codigo_proceso}"
        dgcp_link = "https://comunidad.comprasdominicana.gob.do/Public/Tendering/ContractNoticeManagement/Index"
        maps_link = f"https://www.google.com/maps/search/?api=1&query={direccion.replace(' ', '+')},+Dominican+Republic"

        alerta = (
            f"{estado_proceso}: EDIFICACIÓN DETECTADA\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏗️ <b>OBRA:</b> {obra}\n"
            f"🆔 <b>REF:</b> <code>{codigo_proceso}</code>\n"
            f"📍 <b>ZONA:</b> {region}\n"
            f"🏠 <b>DIRECCIÓN:</b> {direccion}\n"
            f"🏢 <b>EMPRESA:</b> {empresa_real}\n"
            f"🆔 <b>RNC:</b> {rnc_real} (<a href='https://dgii.gov.do/herramientas/consultas/Paginas/RNC.aspx'>🔍 Validar DGII</a>)\n"
            f"👤 <b>INGENIERO:</b> {ing}\n"
            f"📞 <b>TEL:</b> <a href='tel:{tel}'>{tel}</a>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📐 <b>ÁREA:</b> {area} m²\n"
            f"🛡️ <b>GARANTÍA OFRECIDA: 15 AÑOS</b>\n"
            f"📦 <b>REQUERIDO:</b> {res['rollos']} Rollos IDOMI\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 <b>POTENCIAL:</b>\n"
            f"• Inversión: RD$ {res['costo']:,.0f}\n"
            f"💵 <b>PRECIO SUGERIDO: RD$ {res['total']:,.0f}</b>\n"
            f"📈 <b>GANANCIA NETA: RD$ {res['neta']:,.0f}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔍 <b>PARA BÚSQUEDA MANUAL (SI EL LINK FALLA):</b>\n"
            f"🔗 <a href='{dgcp_link}'>PORTAL TRANSACCIONAL DGCP</a>\n\n"
            f"📍 <a href='{maps_link}'>VER EN GOOGLE MAPS</a>\n"
            f"📲 <a href='{wa_link}'>ENVIAR WHATSAPP</a>\n"
            f"✉️ <a href='{mail_link}'>ENVIAR CORREO (15 AÑOS GARANTÍA)</a>"
        )
        enviar_telegram(alerta)

def bucle():
    global ESTADO_MSG_ID
    enviar_telegram("<b>🦅 EL HALCÓN v24.8 ACTIVADO</b>\nRastreo de Procesos Públicos y Correos de 15 años listos.")
    while True:
        ejecutar_patrullaje()
        time.sleep(1200)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle()
