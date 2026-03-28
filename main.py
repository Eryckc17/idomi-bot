import os, time, requests, datetime
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home():
    return "🛡️ IDOMI v16.2 - OPERATIVO"

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
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/deleteMessage", json={"chat_id": CHAT_ID, "message_id": msg_estado_id}, timeout=5)
        except:
            pass
    res = requests.post(url, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "HTML", "disable_web_page_preview": True}, timeout=20)
    if not persistente and res.status_code == 200:
        msg_estado_id = res.json().get("result").get("message_id")

def obtener_tasa():
    try:
        return requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()['rates']['DOP']
    except:
        return 61.25

def ejecutar_vigilancia():
    ahora_rd = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=4)
    hora_f = ahora_rd.strftime('%I:%M %p')
    tasa = obtener_tasa()
    reporte = f"<b>🕵️ VIGILANTE IDOMI v16.2</b>\n━━━━━━━━━━━━━━\n🕒 Hora RD: {hora_f}\n💵 Tasa: {tasa:.2f}\n🔍 Buscando: Licitaciones y Privados\n━━━━━━━━━━━━━━"
    enviar_mensaje(reporte, persistente=False)
    try:
        response = requests.get(URL_DGCP, timeout=30)
        if response.status_code == 200:
            html = response.text.lower()
            if any(k in html for k in ["lona", "asfaltica", "impermeabilizacion", "techado"]):
                es_alum = "aluminio" in html or "aluminizada" in html
                precio = 1150 if es_alum else 850
                monto_dop = 400 * precio
                alerta = f"🚨 <b>PROYECTO DETECTADO</b>\n━━━━━━━━━━━━━━\n💰 Estimado: RD$ {monto_dop:,.2f}\n🔗 <a href='{URL_DGCP}'>LINK DIRECTO</a>\n━━━━━━━━━━━━━━"
                enviar_mensaje(alerta, persistente=True)
    except:
        pass

def bucle_tiempos():
    enviar_mensaje("<b>🚀 SISTEMA v16.2 ACTIVADO</b>", persistente=True)
    while True:
        ejecutar_vigilancia()
        ahora = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=4)).hour
        espera = 900 if 7 <= ahora <= 18 else 3600
        time.sleep(espera)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle_tiempos()
