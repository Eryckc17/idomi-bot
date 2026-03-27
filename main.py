import os, time, requests, datetime
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home(): return "🛡️ IDOMI ULTRA v11.5 - CÁLCULO BIMONETARIO ACTIVO"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN ---
TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
URL_BASE = "https://dgcp.gob.do/servicios/consultar-compras-menores/"
TASA_CAMBIO = 61.50 # DOP por 1 USD (Marzo 2026)

def enviar_alerta(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "HTML", "disable_web_page_preview": True}, timeout=20)

def analizar_ultra_bimonetario():
    headers = {"User-Agent": "Mozilla/5.0"}
    ahora_rd = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=4)
    hora_f = ahora_rd.strftime('%I:%M %p')
    
    try:
        response = requests.get(URL_BASE, headers=headers, timeout=30)
        if response.status_code == 200:
            html = response.text.lower()
            
            if any(k in html for k in ["lona", "asfaltica", "impermeabilizacion", "techado"]):
                # --- CLASIFICACIÓN ---
                es_alum = any(x in html for x in ["aluminizada", "aluminio"])
                es_cibao = any(x in html for x in ["vega", "santiago", "moca", "bonao"])
                es_pub = "ministerio" in html or "escuela" in html or "hospital" in html
                
                # --- CÁLCULO DE POTENCIAL FINANCIERO ---
                # Estimación base: Proyecto de 400 m2 a RD$ 1,150/m2 (Aluminizada Premium)
                monto_dop = 460000 
                monto_usd = monto_dop / TASA_CAMBIO
                
                formato_dop = f"RD$ {monto_dop:,.2f}"
                formato_usd = f"US$ {monto_usd:,.2f}"
                
                color = "🔵 DIAMANTE" if es_alum else "🔴 PRIVADO CIBAO" if es_cibao and not es_pub else "🟢 PÚBLICO"
                
                # --- ESTRUCTURA DEL MENSAJE ---
                mensaje = (
                    f"{color}\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🏗️ <b>PROYECTO:</b> DETECTADO EN PORTAL\n"
                    f"📏 <b>ÁREA:</b> Escala Industrial (> 200 m²)\n"
                    f"📍 <b>ZONA:</b> {'Cibao Central' if es_cibao else 'Nacional'}\n\n"
                    f"💰 <b>POTENCIAL ESTIMADO:</b>\n"
                    f"• <b>{formato_dop}</b>\n"
                    f"• (<b>{formato_usd}</b>)\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"👤 <b>CONTACTO DIRECTO:</b>\n"
                    f"• 📞 <b>Tel:</b> (809) 682-7407\n"
                    f"• 📧 <b>Mail:</b> compras@dgcp.gob.do\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"💡 <b>PITCH:</b> <i>'Nuestra lona aluminizada reduce 15% calor y consumo eléctrico.'</i>\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🔗 <a href='{URL_BASE}'>LINK AL PROYECTO</a>\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🕒 <i>Sincronizado: {hora_f}</i>"
                )
                enviar_alerta(mensaje)
    except: pass

def bucle():
    enviar_alerta("<b>🚀 IDOMI ULTRA v11.5 ONLINE</b>\nPotencial financiero bimonetario activado (RD$ / US$).")
    while True:
        analizar_ultra_bimonetario()
        # Horario laboral cada 15 min, noche cada 1 hora
        ahora = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=4)).hour
        espera = 900 if 7 <= ahora <= 18 else 3600
        time.sleep(espera)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle()
