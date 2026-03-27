import os, time, requests, datetime
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home(): return "🛡️ SISTEMA IDOMI OMNISCIENTE v12.0 - OPERATIVO 24/7"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN DE PODER ---
TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
URL_BASE = "https://dgcp.gob.do/servicios/consultar-compras-menores/"
TASA_CAMBIO = 61.50 # Ajustable según el mercado

# --- BASE DE DATOS ESTRATÉGICA ---
EXCLUSIVAS = ["aluminizada", "aluminio", "aislamiento termico", "reflejante"]
CIBAO_ZONAS = ["vega", "santiago", "moca", "bonao", "san francisco"]
GRANDES_CONST = {
    "bisono": {"tel": "(809) 548-6353", "mail": "proyectos@bisono.com.do", "enc": "Ing. Residente"},
    "estrella": {"tel": "(809) 247-3434", "mail": "info@estrella.com.do", "enc": "Dpto. Licitaciones"},
    "tecasa": {"tel": "(809) 582-1244", "mail": "ventas@tecasa.com.do", "enc": "Gerencia Proyectos"},
    "teddy": {"tel": "(809) 581-2222", "mail": "ingenieria@teddy.com.do", "enc": "Ing. de Compras"}
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

def analizar_mercado_completo():
    headers = {"User-Agent": "Mozilla/5.0"}
    ahora_rd = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=4)
    hora_f = ahora_rd.strftime('%I:%M %p')
    
    # Dashboard de Control
    gestionar_estado(f"<b>🕵️ VIGILANTE IDOMI v12.0</b>\n🕒 Hora RD: {hora_f}\n🚀 Estado: Escaneando Licitaciones, Privados y Mapas...")

    try:
        response = requests.get(URL_BASE, headers=headers, timeout=30)
        if response.status_code == 200:
            html = response.text.lower()
            
            # Solo si detecta palabras clave de impermeabilización
            if any(k in html for k in ["lona", "asfaltica", "impermeabilizacion", "techado", "filtracion"]):
                
                # 1. DETERMINAR PRIORIDAD Y COLOR
                es_alum = any(x in html for x in EXCLUSIVAS)
                es_cibao = any(x in html for x in CIBAO_ZONAS)
                es_pub = any(x in html for x in ["ministerio", "escuela", "hospital", "ayuntamiento", "gobierno"])
                es_grande = any(x in html for x in GRANDES_CONST.keys())

                if es_alum: 
                    color, emoji = "🔵 <b>DIAMANTE (ALUMINIZADA)</b>", "💎"
                elif es_cibao and not es_pub: 
                    color, emoji = "🔴 <b>PRIVADO CIBAO (>200m2)</b>", "🏠"
                elif es_pub: 
                    color, emoji = "🟢 <b>ESTADO (PÚBLICO NACIONAL)</b>", "🏛️"
                elif es_grande: 
                    color, emoji = "🟡 <b>GRANDES LIGAS (NACIONAL)</b>", "🏗️"
                else: 
                    color, emoji = "⚪ <b>INFORMATIVO (ESCALA MENOR)</b>", "📄"

                # 2. CÁLCULO DE DINERO (Estimación base 400m2)
                precio_m2 = 1150 if es_alum else 850
                monto_dop = 400 * precio_m2
                monto_usd = monto_dop / TASA_CAMBIO

                # 3. BUSCAR CONTACTO ESPECÍFICO
                emp_detectada = next((c for c in GRANDES_CONST if c in html), "dgcp")
                cont = GRANDES_CONST.get(emp_detectada, {"tel": "(809) 682-7407", "mail": "compras@dgcp.gob.do", "enc": "Encargado de Compras"})

                # 4. CONSTRUCCIÓN DE LA FICHA MAESTRA
                mensaje = (
                    f"{emoji} {color}\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🏗️ <b>PROYECTO:</b> DETECTADO EN RED\n"
                    f"📏 <b>ÁREA:</b> Escala Industrial (> 200 m²)\n"
                    f"📍 <b>UBICACIÓN:</b> {'Cibao Central (Radio 30km)' if es_cibao else 'Nacional'}\n\n"
                    f"💰 <b>FACTURACIÓN EST.:</b>\n"
                    f"• <b>RD$ {monto_dop:,.2f}</b>\n"
                    f"• (<b>US$ {monto_usd:,.2f}</b>)\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"👤 <b>CONTACTO DIRECTO:</b>\n"
                    f"• <b>Resp:</b> {cont['enc']}\n"
                    f"• 📞 <b>Tel:</b> {cont['tel']}\n"
                    f"• 📧 <b>Mail:</b> {cont['mail']}\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"💡 <b>PITCH:</b> <i>'Nuestra lona aluminizada exclusiva reduce 15% calor y consumo eléctrico.'</i>\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🔗 <a href='{URL_BASE}'>LINK DIRECTO AL PROYECTO</a>\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🕒 <i>Detectado: {hora_f}</i>"
                )
                enviar_alerta(mensaje)
    except: pass

def bucle_infinito():
    enviar_alerta("<b>🔥 IDOMI v12.0 DESPLEGADO</b>\nTodo el sistema de inteligencia comercial está operativo 24/7.")
    while True:
        analizar_mercado_completo()
        # Tiempo adaptativo
        ahora = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=4)).hour
        espera = 900 if 7 <= ahora <= 18 else 3600
        time.sleep(espera)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle_infinito()
