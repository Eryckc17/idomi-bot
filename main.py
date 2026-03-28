import os, time, requests, datetime
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home(): return "🛡️ IDOMI ESTRATÉGICO v16.1 - 24/7 ACTIVO"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
URL_DGCP = "https://dgcp.gob.do/servicios/consultar-compras-menores/"

msg_estado_id = None

def enviar_mensaje(texto, persistente=False):
    global msg_estado_id
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    if not persistente and msg_estado_id:
        try: requests.post(f"https://api.telegram.org/bot{TOKEN}/deleteMessage", 
                          json={"chat_id": CHAT_ID, "message_id": msg_estado_id}, timeout=5)
        except: pass
    res = requests.post(url, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "HTML", "disable_web_page_preview": True}, timeout=20)
    if not persistente and res.status_code == 200:
        msg_estado_id = res.json().get("result").get("message_id")

def obtener_tasa():
    try: return requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()['rates']['DOP']
    except: return 61.25

def ejecutar_vigilancia():
    ahora_rd = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=4)
    hora_f = ahora_rd.strftime('%I:%M %p')
    tasa = obtener_tasa()
    
    reporte = (
        f"<b>🕵️ VIGILANTE IDOMI - ESCANEO EN CURSO</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🕒 <b>Hora RD:</b> {hora_f}\n"
        f"💵 <b>Tasa USD/DOP:</b> {tasa:.2f}\n\n"
        f"🔎 <b>BUSCANDO EN:</b>\n"
        f"• 🏛️ Licitaciones Públicas (DGCP)\n"
        f"• 🏗️ Constructoras (Bisonó, Estrella, etc.)\n\n"
        f"🎯 <b>FILTRO:</b> Lona / Impermeabilización\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    enviar_mensaje(reporte, persistente=False)

    try:
        response = requests.get(URL_DGCP, timeout=30)
        if response.status_code == 200:
            html = response.text.lower()
            # SECCIÓN CORREGIDA DE ESPACIOS
            if any(k in html for k in ["lona", "asfaltica", "impermeabilizacion", "techado"]):
                es_alum = "aluminio" in html or "aluminizada" in html
                precio = 1150 if es_alum else 850
                monto_dop = 400 * precio
                alerta = (
                    f"🚨 <b>PROYECTO DETECTADO</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"💰 <b>ESTIMADO:</b> RD$ {monto_dop:,.2f}\n"
                    f"🔗 <a href='{URL_DGCP}'>LINK DIRECTO</a>\n"
                    f"━━━━━━━━━━━━━━━━━━━━"
                )
                enviar_mensaje(alerta, persistente=True)
    except: pass

def bucle_tiempos():
    enviar_mensaje("<b>🚀 SISTEMA v16.1 ACTIVADO</b>\nPatrullaje dominicano iniciado.", persistente=True)
    while True:
        ejecutar_vigilancia()
        ahora = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=4)).hour
        espera = 900 if 7 <= ahora <= 18 else 3600
        time.sleep(espera)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle_tiempos()
                    f"🚨 <b>PROYECTO DETECTADO</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"💰 <b>ESTIMADO:</b> RD$ {monto_dop:,.2f}\n"
                    f"🔗 <a href='{URL_DGCP}'>LINK DIRECTO</a>\n"
                    f"━━━━━━━━━━━━━━━━━━━━"
                )
                enviar_mensaje(alerta, persistente=True)
    except: pass

def bucle_tiempos():
    enviar_mensaje("<b>🚀 SISTEMA v16.0 ACTIVADO</b>\nIDOMI está patrullando el mercado dominicano.", persistente=True)
    while True:
        ejecutar_vigilancia()
        
        # --- LÓGICA DE TIEMPOS ACORDADA ---
        ahora = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=4)).hour
        
        if 7 <= ahora <= 18:
            # Horario Laboral: Cada 15 min (900 seg)
            time.sleep(900)
        else:
            # Horario Nocturno: Cada 1 hora (3600 seg) - Nunca se para
            time.sleep(3600)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle_tiempos()
            
            if any(k in contenido for k in ["lona", "asfaltica", "impermeabilizacion", "techado"]):
                # Clasificación por Colores
                es_alum = any(x in contenido for x in ["aluminio", "aluminizada"])
                es_cibao = any(x in contenido for x in ["vega", "santiago", "moca", "bonao"])
                es_pub = any(x in contenido for x in ["ministerio", "escuela", "hospital", "ayuntamiento"])

                if es_alum: color, emoji = "🔵 <b>DIAMANTE (ALUMINIZADA)</b>", "💎"
                elif es_cibao and not es_pub: color, emoji = "🔴 <b>PRIVADO CIBAO</b>", "🏠"
                elif es_pub: color, emoji = "🟢 <b>ESTADO PÚBLICO RD</b>", "🏛️"
                else: color, emoji = "🟡 <b>GRANDE NACIONAL</b>", "🏗️"

                # Cálculo de Dinero en Pesos Dominicanos (Base 400m2)
                precio_m2 = 1150 if es_alum else 850
                monto_dop = 400 * precio_m2
                monto_usd = monto_dop / tasa_dop

                emp_clave = next((c for c in GRANDES_CONST if c in contenido), "dgcp")
                info = GRANDES_CONST[emp_clave]

                mensaje = (
                    f"{emoji} {color}\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🏗️ <b>PROYECTO:</b> DETECTADO EN RD\n"
                    f"📏 <b>ÁREA ESTIMADA:</b> > 200 m²\n"
                    f"💰 <b>POTENCIAL (TASA {tasa_dop:.2f}):</b>\n"
                    f"• <b>RD$ {monto_dop:,.2f}</b>\n"
                    f"• (<b>US$ {monto_usd:,.2f}</b>)\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"👤 <b>CONTACTO:</b>\n"
                    f"• 📞 <b>Tel:</b> {info['tel']}\n"
                    f"• 📧 <b>Mail:</b> {info['mail']}\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"💡 <b>PITCH:</b> <i>'Lona aluminizada IDOMI: Calidad superior para el clima dominicano.'</i>\n"
                    f"🔗 <a href='{URL_PORTAL}'>VER EXPEDIENTE EN DGCP</a>\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🕒 <i>Detectado: {hora_f}</i>"
                )
                enviar_alerta(mensaje)
    except: pass

def bucle_rd():
    enviar_alerta("<b>🇩🇴 IDOMI RD v14.0 DESPLEGADO</b>\nSistema 100% dominicano con tasa USD/DOP en vivo.")
    while True:
        analizar_mercado_rd()
        ahora = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=4)).hour
        espera = 900 if 7 <= ahora <= 18 else 3600
        time.sleep(espera)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle_rd()
