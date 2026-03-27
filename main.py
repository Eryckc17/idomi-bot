import os, time, requests, datetime
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home(): return "🛡️ IDOMI DOMINICANA v14.0 - MERCADO RD ACTIVO"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN DOMINICANA ---
TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
URL_PORTAL = "https://dgcp.gob.do/servicios/consultar-compras-menores/"

# --- FUNCIÓN DE TASA DOP EN VIVO ---
def obtener_tasa_dop():
    try:
        # Obtiene la tasa oficial de mercado para el Peso Dominicano
        res = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
        data = res.json()
        return data['rates']['DOP'] 
    except:
        return 61.20 # Tasa de seguridad si la API falla

# --- BASE DE DATOS DE CONSTRUCTORAS RD ---
GRANDES_CONST = {
    "bisono": {"tel": "(809) 548-6353", "mail": "proyectos@bisono.com.do", "enc": "Dpto. Ingeniería"},
    "estrella": {"tel": "(809) 247-3434", "mail": "info@estrella.com.do", "enc": "Gerencia de Proyectos"},
    "tecasa": {"tel": "(809) 582-1244", "mail": "ventas@tecasa.com.do", "enc": "Ingeniero de Obra"},
    "dgcp": {"tel": "(809) 682-7407", "mail": "compras@dgcp.gob.do", "enc": "Unidad de Adquisiciones"}
}

ultimo_mensaje_id = None

def enviar_alerta(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "HTML", "disable_web_page_preview": True}, timeout=20)

def gestionar_estado(mensaje):
    global ultimo_mensaje_id
    base_url = f"https://api.telegram.org/bot{TOKEN}"
    if ultimo_mensaje_id:
        try: requests.post(f"{base_url}/deleteMessage", json={"chat_id": CHAT_ID, "message_id": ultimo_mensaje_id}, timeout=5)
        except: pass
    res = requests.post(f"{base_url}/sendMessage", json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML"}, timeout=10)
    if res.status_code == 200:
        ultimo_mensaje_id = res.json().get("result").get("message_id")

def analizar_mercado_rd():
    headers = {"User-Agent": "Mozilla/5.0"}
    # Ajuste de hora fija para República Dominicana (UTC-4)
    ahora_rd = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=4)
    hora_f = ahora_rd.strftime('%I:%M %p')
    
    tasa_dop = obtener_tasa_dop()
    
    gestionar_estado(f"<b>🕵️ VIGILANTE IDOMI RD</b>\n🕒 Hora: {hora_f}\n💵 Tasa USD/DOP: <b>{tasa_dop:.2f}</b>\n✅ Escaneando: Licitaciones y Proyectos...")

    try:
        response = requests.get(URL_PORTAL, headers=headers, timeout=30)
        if response.status_code == 200:
            contenido = response.text.lower()
            
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
