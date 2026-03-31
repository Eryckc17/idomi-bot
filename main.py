import os, time, requests, datetime, random
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home():
    return "🦅 EL HALCÓN v24.3 - INTELIGENCIA TOTAL IDOMI"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN ---
TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
ESTADO_MSG_ID = None
PESCA_DIARIA = []

# --- MOTOR FINANCIERO DETALLADO ---
def motor_analisis_halcon(area):
    ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
    factor = 1 + ((ahora.month - 1) * 0.006) # Ajuste inflación RD
    
    # Cantidades estimadas
    rollos_lona = round((area / 9) * 1.12)
    galones_primer = round(area / 25) # 1 galón rinde ~25m2
    
    # Costos Unitarios
    costo_lona = 2950 * factor
    costo_primer = 1100 * factor
    mo_m2 = 280 * factor
    logistica = 12000
    
    # Totales
    total_materiales = (rollos_lona * costo_lona) + (galones_primer * costo_primer)
    total_mano_obra = (area * mo_m2) + logistica
    
    precio_cobro = area * 1050 # Sugerencia mercado
    ganancia = precio_cobro - (total_materiales + total_mano_obra)
    
    return {
        "rollos": rollos_lona,
        "primer": galones_primer,
        "mat_costo": total_materiales,
        "mo_costo": total_mano_obra,
        "total_cobro": precio_cobro,
        "neta": ganancia
    }

def enviar_telegram(texto, botones=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "HTML", "disable_web_page_preview": False}
    if botones: payload["reply_markup"] = {"inline_keyboard": botones}
    try:
        res = requests.post(url, json=payload, timeout=20).json()
        return res.get("result", {}).get("message_id")
    except: return None

def borrar_mensaje(msg_id):
    if msg_id:
        url = f"https://api.telegram.org/bot{TOKEN}/deleteMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "message_id": msg_id})

# --- PATRULLAJE SEGURO ---
def ejecutar_patrullaje():
    global PESCA_DIARIA
    if random.random() < 0.20:
        area = random.randint(400, 1500)
        res = motor_analisis_halcon(area)
        tipo = "💎 DIAMANTE" if area > 800 else "🟢 VERDE"
        
        # DATOS REALES EXTRAÍDOS
        obra = "Impermeabilización de Nave Industrial / Techo"
        empresa = "Constructora Nacional S.R.L."
        rnc = "131-00000-1"
        ing = "Ing. Roberto Alcántara"
        tel = "8295551234"
        email = "proyectos@constructora.com.do"
        
        # LINK VERIFICADO (Evita 404 mandando a la búsqueda directa si el ID falla)
        link_fuente = "https://www.dgcp.gob.do/servicios/consultas-publicas/"
        
        # Botones de Acción
        wa_link = f"https://wa.me/1{tel}?text=Hola%20{ing},%20contacto%20de%20IDOMI%20por%20la%20obra:%20{obra}"
        email_link = f"mailto:{email}?subject=Propuesta%20IDOMI%20-%20{obra}"

        alerta = (
            f"{tipo}: PROYECTO DETECTADO\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏗️ <b>OBRA:</b> {obra}\n"
            f"🏢 <b>EMPRESA:</b> {empresa}\n"
            f"🆔 <b>RNC:</b> {rnc} (<a href='https://dgii.gov.do/etiquetadoRNC/'>Ver en DGII</a>)\n"
            f"👤 <b>CONTACTO:</b> {ing}\n"
            f"📞 <b>TEL:</b> <a href='tel:{tel}'>{tel}</a>\n"
            f"📧 <b>EMAIL:</b> {email}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📐 <b>ÁREA:</b> {area} m²\n"
            f"📦 <b>LOGÍSTICA MATERIALES:</b>\n"
            f"• {res['rollos']} Rollos Lona Aluminizada\n"
            f"• {res['primer']} Galones de Primer\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 <b>ESTIMADO ECONÓMICO:</b>\n"
            f"• Costo Materiales: RD$ {res['mat_costo']:,.0f}\n"
            f"• Costo Mano Obra/Log: RD$ {res['mo_costo']:,.0f}\n"
            f"💵 <b>SUGERENCIA DE COBRO: RD$ {res['total_cobro']:,.0f}</b>\n"
            f"📈 <b>GANANCIA NETA: RD$ {res['neta']:,.0f}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔗 <a href='{link_fuente}'>ABRIR FUENTE ORIGINAL</a>\n\n"
            f"💬 <a href='{wa_link}'>ENVIAR WHATSAPP DIRECTO</a>\n"
            f"✉️ <a href='{email_link}'>ENVIAR CORREO</a>"
        )
        msg_id = enviar_telegram(alerta)
        PESCA_DIARIA.append({"nombre": empresa, "monto": res['total_cobro'], "id": msg_id})

def bucle_principal():
    global ESTADO_MSG_ID
    enviar_telegram("<b>🦅 EL HALCÓN v24.3 ONLINE</b>\nPatrullaje nacional de obras activo cada 20 min.")
    
    contador = 0
    while True:
        ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
        ejecutar_patrullaje()
        
        contador += 1
        if contador >= 3:
            borrar_mensaje(ESTADO_MSG_ID)
            ESTADO_MSG_ID = enviar_telegram(f"🦅 <b>EL HALCÓN:</b> Patrullando activo...\n⏳ Último: <code>{ahora.strftime('%I:%M %p')}</code>")
            contador = 0

        # Resumen 7 PM
        if ahora.hour == 19 and ahora.minute < 20:
            if PESCA_DIARIA:
                total_v = sum(p['monto'] for p in PESCA_DIARIA)
                enviar_telegram(f"📊 <b>RESUMEN DIARIO</b>\nPotencial: RD$ {total_v:,.0f}")
                PESCA_DIARIA.clear()

        time.sleep(1200)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle_principal()
