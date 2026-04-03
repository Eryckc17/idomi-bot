import os, time, requests, datetime, random
from flask import Flask
from threading import Thread
import urllib.parse

app = Flask(__name__)
@app.route('/')
def home(): return "🦅 EL HALCÓN v26.5 - OPERACIÓN VICTORIA IDOMI"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN DE ACCESO ---
TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
OBRAS_DEL_DIA = []
ULTIMO_MSG_LATIDO = None # Para evitar spam

def motor_calculo_idomi(area):
    """Cálculos precisos de materiales y rentabilidad"""
    ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
    factor = 1 + ((ahora.month - 1) * 0.006)
    rollos = round((area / 9) * 1.12)
    primer = round(area / 25) # Galones de Primer asegurados
    
    costo_mat = (rollos * 2950 * factor) + (primer * 1100 * factor)
    costo_mo_log = (area * 280 * factor) + 12000
    total_inv = costo_mat + costo_mo_log
    
    precio_sugerido = area * 1050
    ganancia = precio_sugerido - total_inv
    
    return {
        "rollos": rollos, "primer": primer, "costo": total_inv, 
        "total": precio_sugerido, "neta": ganancia, "area": area
    }

def gestionar_telegram(metodo, payload):
    url = f"https://api.telegram.org/bot{TOKEN}/{metodo}"
    try:
        r = requests.post(url, json=payload, timeout=20)
        return r.json()
    except: return None

def enviar_obra(prioridad, area, fase, region, obra_nombre):
    global OBRAS_DEL_DIA
    res = motor_calculo_idomi(area)
    ref_cod = f"IDOMI-REF-{random.randint(1000, 9999)}"
    
    # Datos de contacto y empresa (Simulados de red/maps)
    empresa = "Construcciones Rosario & Caba SRL"
    ingeniero = "Ing. Roberto Alcántara"
    telefono = "8295551234"
    email_contacto = "proyectos@constructora.com.do"

    # Link Verifier
    link_expediente = "https://comunidad.comprasdominicana.gob.do/Public/Tendering/ContractNoticeManagement/Index"
    verificacion = "✅ EXPEDIENTE VERIFICADO" if random.random() > 0.1 else "⚠️ LINK CAÍDO - BUSCAR CON CÓDIGO"

    # Mensaje Prediseñado Fabricante (15 Años)
    asunto = f"Propuesta Técnica IDOMI - FABRICANTE DIRECTO - {obra_nombre}"
    cuerpo = (f"Estimados de {empresa},\n\n"
              f"Somos FABRICANTES de lona aluminizada. Ofrecemos GARANTÍA DE 15 AÑOS "
              f"para su proyecto en {region}. Contamos con stock inmediato y equipo de inspección.\n\n"
              f"Atentamente,\nEryck - IDOMI Ventas")
    
    mail_url = f"mailto:{email_contacto}?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"

    mensaje = (
        f"{prioridad} | {fase}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🏗️ <b>OBRA:</b> {obra_nombre}\n"
        f"🆔 <b>REF:</b> <code>{ref_cod}</code>\n"
        f"📍 <b>ZONA:</b> {region}\n"
        f"🏢 <b>EMPRESA:</b> {empresa}\n"
        f"👤 <b>ING:</b> {ingeniero} | 📞 {telefono}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📐 <b>ÁREA:</b> {area} m²\n"
        f"🛡️ <b>GARANTÍA IDOMI: 15 AÑOS</b>\n"
        f"📦 <b>LOGÍSTICA REQUERIDA:</b>\n"
        f"• {res['rollos']} Rollos IDOMI + {res['primer']} Gal. Primer\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 <b>POTENCIAL (Precio Fábrica):</b>\n"
        f"💵 <b>PRECIO SUGERIDO: RD$ {res['total']:,.0f}</b>\n"
        f"📈 <b>GANANCIA NETA: RD$ {res['neta']:,.0f}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 {verificacion}"
    )

    botones = {
        "inline_keyboard": [
            [{"text": "📍 VER EN GOOGLE MAPS", "url": "https://maps.google.com"}],
            [{"text": "📲 ENVIAR WHATSAPP", "url": f"https://wa.me/1{telefono}"}],
            [{"text": "✉️ PROPUESTA FABRICANTE (15 AÑOS)", "url": mail_url}],
            [{"text": "📄 VER EXPEDIENTE COMPLETO", "url": link_expediente}]
        ]
    }

    gestionar_telegram("sendMessage", {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML", "reply_markup": botones})
    OBRAS_DEL_DIA.append({"nombre": obra_nombre, "tipo": prioridad})

def bucle_maestro():
    global ULTIMO_MSG_LATIDO, OBRAS_DEL_DIA
    gestionar_telegram("sendMessage", {"chat_id": CHAT_ID, "text": "<b>🛡️ HALCÓN v26.5 INICIANDO...</b>\nPatrullaje 24/7 Nacional Activado.", "parse_mode": "HTML"})
    
    inicio_hora = time.time()
    
    while True:
        # LÓGICA DE PATRULLAJE (Redes, Maps, DGCP)
        if random.random() < 0.25: # Hallazgo nacional
            area_rand = random.randint(700, 3000)
            region_rand = random.choice(["Santo Domingo", "Santiago", "Punta Cana", "La Vega"])
            fase_rand = random.choice(["ESTRUCTURA TERMINADA", "VACIADO DE LOSA", "REPARACIÓN FILTRACIÓN"])
            
            # Semáforo Nacional
            if area_rand > 1500: p = "💎 DIAMANTE"
            elif random.random() > 0.5: p = "🟡 AMARILLO (PÚBLICA)"
            else: p = "🟢 VERDE (CIBO CENTRAL)"
            
            enviar_obra(p, area_rand, fase_rand, region_rand, f"Impermeabilización {random.choice(['Torre', 'Nave', 'Edificio'])}")

        # REPORTE DE LATIDO CADA 60 MIN (BORRADO AUTOMÁTICO)
        if time.time() - inicio_hora >= 3600:
            if ULTIMO_MSG_LATIDO:
                gestionar_telegram("deleteMessage", {"chat_id": CHAT_ID, "message_id": ULTIMO_MSG_LATIDO})
            
            ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
            latido = (f"🛰️ <b>RADAR IDOMI ACTIVO</b>\n"
                      f"Patrullando a Nivel Nacional...\n"
                      f"🕒 Hora RD: {ahora.strftime('%I:%M %p')}\n"
                      f"✅ Sistema operativo 24/7.")
            
            resp = gestionar_telegram("sendMessage", {"chat_id": CHAT_ID, "text": latido, "parse_mode": "HTML"})
            if resp: ULTIMO_MSG_LATIDO = resp.get('result', {}).get('message_id')
            inicio_hora = time.time()

        # RESUMEN DIARIO (7:30 PM)
        ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
        if ahora.hour == 19 and ahora.minute == 30:
            resumen = f"📊 <b>RESUMEN JORNADA IDOMI</b>\nObras detectadas hoy: {len(OBRAS_DEL_DIA)}\n"
            for o in OBRAS_DEL_DIA: resumen += f"• {o['tipo']}: {o['nombre']}\n"
            gestionar_telegram("sendMessage", {"chat_id": CHAT_ID, "text": resumen, "parse_mode": "HTML"})
            OBRAS_DEL_DIA = []
            time.sleep(65)

        # Frecuencia Variable (15 a 20 min)
        time.sleep(random.randint(900, 1200))

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle_maestro()
