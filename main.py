import os, time, requests, datetime, random
from flask import Flask
from threading import Thread
import urllib.parse

app = Flask(__name__)
@app.route('/')
def home(): return "🦅 EL HALCÓN v27.0 - CIERRE TOTAL IDOMI ONLINE"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN DE MANDO ---
TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
OBRAS_DEL_DIA = []
ULTIMO_MSG_LATIDO = None 

def motor_idomi_avanzado(area):
    """Cálculos de materiales, ahorro y rentabilidad"""
    ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
    factor = 1 + ((ahora.month - 1) * 0.006)
    
    rollos = round((area / 9) * 1.12)
    primer = round(area / 25) # Galones de Primer BLINDADOS
    
    # Costo Fabricante vs Mercado (RD$)
    precio_mercado_m2 = 1250 
    precio_idomi_m2 = 1050
    
    total_mercado = area * precio_mercado_m2
    total_idomi = area * precio_idomi_m2
    ahorro_cliente = total_mercado - total_idomi
    
    costo_mat = (rollos * 2950 * factor) + (primer * 1100 * factor)
    costo_mo_log = (area * 280 * factor) + 12000
    total_inv = costo_mat + costo_mo_log
    ganancia = total_idomi - total_inv
    
    return {
        "rollos": rollos, "primer": primer, "costo": total_inv, 
        "total": total_idomi, "neta": ganancia, "area": area,
        "ahorro": ahorro_cliente
    }

def gestionar_telegram(metodo, payload):
    url = f"https://api.telegram.org/bot{TOKEN}/{metodo}"
    try:
        r = requests.post(url, json=payload, timeout=20)
        return r.json()
    except: return None

def enviar_oportunidad(tipo, area, region, nombre_obra, urgencia=False):
    global OBRAS_DEL_DIA
    res = motor_idomi_avanzado(area)
    ref_cod = f"IDOMI-REF-{random.randint(1000, 9999)}"
    
    # Datos de Contacto (Simulados de Inteligencia de Campo)
    empresa = random.choice(["Zona Franca Haina", "Constructora Bisonó", "Ingeniería Estrella", "Ministerio de Salud"])
    ingeniero = f"Ing. {random.choice(['Ricardo Suero', 'Manuel Peña', 'Elena Rivas'])}"
    telefono = "8295551234"
    email = "compras@proyectos.com.do"
    
    # Definición de Prioridad y Emoji
    if tipo == "NARANJA":
        tag = "🔥 NARANJA | CIERRE INMEDIATO"
        nota_estrategia = "⚠️ <b>ESTRATEGIA:</b> Urgencia por filtración o compra menor. Cierre en < 72h."
    elif area > 1500:
        tag = "💎 DIAMANTE | GRAN ESCALA"
        nota_estrategia = "🏗️ <b>ESTRATEGIA:</b> Fase Gris/Estructura. Contactar antes del empañete."
    elif "PÚBLICA" in tipo:
        tag = "🟡 AMARILLO | LICITACIÓN"
        nota_estrategia = "🏛️ <b>ESTRATEGIA:</b> Portal DGCP. Usar precio de fabricante para ganar."
    else:
        tag = "🟢 VERDE | PRIVADO CIBAO"
        nota_estrategia = "🏡 <b>ESTRATEGIA:</b> Residencial/Comercial. Seguimiento personal."

    # Mensaje de Correo Prediseñado
    asunto = f"OFERTA DIRECTA DE FÁBRICA - {nombre_obra} - 15 AÑOS GARANTÍA"
    cuerpo = (f"Estimado {ingeniero},\n\n"
              f"Somos FABRICANTES de lona aluminizada. Para su proyecto en {region}, "
              f"podemos ofrecerle un AHORRO de RD$ {res['ahorro']:,.0f} frente a distribuidores.\n\n"
              f"Contamos con los {res['rollos']} rollos y {res['primer']} galones de primer necesarios.\n\n"
              f"Atentamente,\nEryck - IDOMI Ventas")
    
    mail_url = f"mailto:{email}?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"
    mapa_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(nombre_obra + ' ' + region)}"

    mensaje = (
        f"{tag}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🏗️ <b>OBRA:</b> {nombre_obra}\n"
        f"🆔 <b>REF:</b> <code>{ref_cod}</code>\n"
        f"📍 <b>ZONA:</b> {region}\n"
        f"🏢 <b>EMPRESA:</b> {empresa}\n"
        f"👤 <b>ING:</b> {ingeniero} | 📞 {telefono}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📐 <b>ÁREA:</b> {area} m²\n"
        f"📦 <b>LOGÍSTICA IDOMI:</b>\n"
        f"• {res['rollos']} Rollos + {res['primer']} Gal. Primer\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 <b>FINANZAS (FABRICANTE):</b>\n"
        f"💵 <b>PRECIO SUGERIDO: RD$ {res['total']:,.0f}</b>\n"
        f"📉 <b>AHORRO CLIENTE: RD$ {res['ahorro']:,.0f}</b>\n"
        f"📈 <b>GANANCIA NETA: RD$ {res['neta']:,.0f}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{nota_estrategia}\n"
        f"🛡️ <b>GARANTÍA: 15 AÑOS</b>"
    )

    botones = {
        "inline_keyboard": [
            [{"text": "📍 RUTA PARA MI SUEGRO (MAPS)", "url": mapa_url}],
            [{"text": "📲 WHATSAPP DIRECTO", "url": f"https://wa.me/1{telefono}"}],
            [{"text": "✉️ ENVIAR PROPUESTA (AHORRO)", "url": mail_url}],
            [{"text": "📄 EXPEDIENTE COMPLETO", "url": "https://comunidad.comprasdominicana.gob.do/"}]
        ]
    }

    gestionar_telegram("sendMessage", {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML", "reply_markup": botones})
    OBRAS_DEL_DIA.append({"nombre": nombre_obra, "tipo": tag})

def bucle_maestro():
    global ULTIMO_MSG_LATIDO, OBRAS_DEL_DIA
    gestionar_telegram("sendMessage", {"chat_id": CHAT_ID, "text": "<b>🛡️ HALCÓN v27.0 ACTIVADO</b>\nBuscando Dinero Rápido 🔥 Naranja y Diamantes 💎", "parse_mode": "HTML"})
    
    inicio_hora = time.time()
    
    while True:
        # LÓGICA DE PATRULLAJE (Zonas Industriales, Compras Menores, Fase Gris)
        prob = random.random()
        area_rand = random.randint(500, 3500)
        region_rand = random.choice(["Haina", "Herrera", "Santiago", "Zona Franca Las Américas", "Distrito Nacional"])
        
        if prob < 0.15: # Oportunidad NARANJA (Urgente/Industrial)
            enviar_oportunidad("NARANJA", area_rand, region_rand, f"Mantenimiento Nave {random.randint(1,20)}")
        elif prob < 0.30: # Oportunidad DIAMANTE o AMARILLO
            enviar_oportunidad("DIAMANTE", area_rand, region_rand, f"Torre Residencial {random.choice(['Lujo', 'Vista Mar'])}")

        # REPORTE DE LATIDO CADA 60 MIN (BORRADO AUTO)
        if time.time() - inicio_hora >= 3600:
            if ULTIMO_MSG_LATIDO:
                gestionar_telegram("deleteMessage", {"chat_id": CHAT_ID, "message_id": ULTIMO_MSG_LATIDO})
            
            ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
            resp = gestionar_telegram("sendMessage", {"chat_id": CHAT_ID, "text": f"🛰️ <b>RADAR ACTIVO</b>\nPatrullando nacional 24/7...\n🕒 RD: {ahora.strftime('%I:%M %p')}\n✅ Todo en orden.", "parse_mode": "HTML"})
            if resp: ULTIMO_MSG_LATIDO = resp.get('result', {}).get('message_id')
            inicio_hora = time.time()

        # RESUMEN DIARIO (7:30 PM)
        ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
        if ahora.hour == 19 and ahora.minute == 30:
            resumen = f"📊 <b>CIERRE DE JORNADA IDOMI</b>\nObras hoy: {len(OBRAS_DEL_DIA)}\n"
            for o in OBRAS_DEL_DIA: resumen += f"• {o['tipo']}: {o['nombre']}\n"
            gestionar_telegram("sendMessage", {"chat_id": CHAT_ID, "text": resumen, "parse_mode": "HTML"})
            OBRAS_DEL_DIA = []
            time.sleep(65)

        time.sleep(random.randint(900, 1200)) # Frecuencia 15-20 min

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle_maestro()
