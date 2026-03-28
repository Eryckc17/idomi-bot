import os, time, requests, datetime
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home():
    return "🛡️ IDOMI v17.0 - VIGILANCIA DISCRETA ACTIVA"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
URL_PORTAL = "https://dgcp.gob.do/servicios/consultar-compras-menores/"
msg_estado_id = None

def enviar_mensaje(texto, persistente=False):
    global msg_estado_id
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Borrar el rastro anterior si no es una alerta de obra
    if not persistente and msg_estado_id:
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/deleteMessage", 
                          json={"chat_id": CHAT_ID, "message_id": msg_estado_id}, timeout=5)
        except:
            pass
            
    res = requests.post(url, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "HTML", "disable_web_page_preview": True}, timeout=20)
    
    if not persistente and res.status_code == 200:
        msg_estado_id = res.json().get("result").get("message_id")

def obtener_tasa():
    try:
        res = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
        return res.json()['rates']['DOP']
    except:
        return 61.35

def ejecutar_rastreo():
    ahora_rd = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=4)
    hora_f = ahora_rd.strftime('%I:%M %p')
    
    # MENSAJE DE ESTADO (Limpio y sin cálculos)
    reporte = (
        f"<b>🕵️ VIGILANTE IDOMI v17.0</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🕒 <b>Último Escaneo:</b> {hora_f}\n"
        f"✅ <b>Estado:</b> Activo y Rastreado\n"
        f"🔍 <b>Filtro:</b> Licitaciones y Privados RD\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Buscando oportunidades de Impermeabilización...</i>"
    )
    enviar_mensaje(reporte, persistente=False)

    try:
        response = requests.get(URL_PORTAL, timeout=30)
        if response.status_code == 200:
            html = response.text.lower()
            
            # Solo si hay hallazgo hacemos cálculos financieros
            if any(k in html for k in ["lona", "asfaltica", "impermeabilizacion", "techado"]):
                tasa = obtener_tasa()
                es_alum = "aluminio" in html or "aluminizada" in html
                precio_m2 = 1180 if es_alum else 875
                monto_dop = 400 * precio_m2
                monto_usd = monto_dop / tasa

                alerta = (
                    f"🚨 <b>¡OPORTUNIDAD DETECTADA!</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🏗️ <b>PROYECTO:</b> Hallazgo en RD\n"
                    f"💰 <b>POTENCIAL ESTIMADO:</b>\n"
                    f"• <b>RD$ {monto_dop:,.2f}</b>\n"
                    f"• (<b>US$ {monto_usd:,.2f}</b>)\n"
                    f"💵 <b>Tasa Aplicada:</b> {tasa:.2f}\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🔗 <a href='{URL_PORTAL}'>VER EXPEDIENTE COMPLETO</a>\n"
                    f"━━━━━━━━━━━━━━━━━━━━"
                )
                enviar_mensaje(alerta, persistente=True)
    except:
        pass

def bucle_infinito():
    enviar_mensaje("<b>🚀 SISTEMA v17.0 ONLINE</b>\nReportes cada 30 min. Tasa solo en alertas.", persistente=True)
    while True:
        ejecutar_rastreo()
        # Espera constante de 30 minutos (1800 segundos)
        time.sleep(1800)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle_infinito()
