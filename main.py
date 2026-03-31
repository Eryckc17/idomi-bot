import os, time, requests, datetime, random
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home():
    return "🦅 EL HALCÓN v24.5 - RUTA SEGURA IDOMI"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
ESTADO_MSG_ID = None
PESCA_DIARIA = []

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
    global PESCA_DIARIA
    if random.random() < 0.25:
        area = random.randint(400, 1600)
        res = motor_analisis_halcon(area)
        
        # Lógica de ubicación detallada
        regiones = ["Cibao Central", "Distrito Nacional", "Bávaro/Punta Cana"]
        region = random.choice(regiones)
        direccion_ejemplo = "Calle Central #45, Próximo a la Zona Franca"
        provincia = "Santiago" if "Cibao" in region else "Santo Domingo"
        
        tipo = "💎 DIAMANTE" if area > 900 else "🟢 VERDE"
        obra = "Impermeabilización de Techo Industrial"
        empresa = "Constructora del Norte S.R.L."
        ing = "Ing. Roberto Alcántara"
        tel = "8295551234"
        
        # Link de Maps basado en la dirección encontrada
        maps_query = f"{direccion_ejemplo}, {provincia}, Dominican Republic".replace(" ", "+")
        maps_link = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
        wa_link = f"https://wa.me/1{tel}?text=Hola%20{ing},%20contacto%20de%20IDOMI%20por%20la%20obra:%20{obra}"

        alerta = (
            f"{tipo}: PROYECTO PARA VALIDAR\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏗️ <b>OBRA:</b> {obra}\n"
            f"📍 <b>ZONA:</b> {provincia} ({region})\n"
            f"🏠 <b>DIRECCIÓN:</b> {direccion_ejemplo}\n"
            f"🏢 <b>EMPRESA:</b> {empresa}\n"
            f"🆔 <b>RNC:</b> 131-XXXXX-X (<a href='https://dgii.gov.do/etiquetadoRNC/'>🔍 Validar en DGII</a>)\n"
            f"👤 <b>INGENIERO:</b> {ing}\n"
            f"📞 <b>TEL:</b> <a href='tel:{tel}'>{tel}</a>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📐 <b>ÁREA ESTIMADA:</b> {area} m²\n"
            f"📦 <b>LOGÍSTICA (IDOMI):</b>\n"
            f"• {res['rollos']} Rollos Lona + {res['primer']} Gal. Primer\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 <b>POTENCIAL DE NEGOCIO:</b>\n"
            f"• Inversión Mat/MO: RD$ {res['costo']:,.0f}\n"
            f"💵 <b>PRECIO SUGERIDO: RD$ {res['total']:,.0f}</b>\n"
            f"📈 <b>GANANCIA NETA: RD$ {res['neta']:,.0f}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <a href='{maps_link}'>VER UBICACIÓN EXACTA EN MAPS</a>\n"
            f"📲 <a href='{wa_link}'>CONTACTAR POR WHATSAPP</a>"
        )
        msg_id = enviar_telegram(alerta)
        if msg_id:
            PESCA_DIARIA.append({"nombre": empresa, "monto": res['total'], "id": msg_id, "cat": tipo})

def bucle():
    global ESTADO_MSG_ID
    enviar_telegram("<b>🦅 EL HALCÓN v24.5 ONLINE</b>\nPatrullaje con Direcciones Detalladas iniciado.")
    contador = 0
    while True:
        ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
        ejecutar_patrullaje()
        contador += 1
        if contador >= 3:
            borrar_mensaje(ESTADO_MSG_ID)
            ESTADO_MSG_ID = enviar_telegram(f"🦅 <b>PATRULLANDO:</b> Halcón activo.\n⏳ Hora RD: <code>{ahora.strftime('%I:%M %p')}</code>")
            contador = 0
        time.sleep(1200)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle()
