import os, time, requests, datetime, random, urllib.parse
from flask import Flask
from threading import Thread
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route('/')
def home(): return "🦅 EL HALCÓN v27.0 - INTELIGENCIA TOTAL NACIONAL"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN DE MANDO ---
TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
OBRAS_PROCESADAS = set() 
ULTIMO_MSG_LATIDO = None 

# 1. MOTOR DE CÁLCULOS IDOMI (Mantenido al 100%)
def motor_idomi_avanzado(area):
    ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
    factor = 1 + ((ahora.month - 1) * 0.006)
    rollos = round((area / 9) * 1.12)
    primer = round(area / 25) 
    precio_mercado_m2, precio_idomi_m2 = 1250, 1050
    total_mercado, total_idomi = area * precio_mercado_m2, area * precio_idomi_m2
    ahorro_cliente = total_mercado - total_idomi
    costo_mat = (rollos * 2950 * factor) + (primer * 1100 * factor)
    costo_mo_log = (area * 280 * factor) + 12000
    total_inv = costo_mat + costo_mo_log
    ganancia = total_idomi - total_inv
    return {"rollos": rollos, "primer": primer, "costo": total_inv, "total": total_idomi, "neta": ganancia, "area": area, "ahorro": ahorro_cliente}

def gestionar_telegram(metodo, payload):
    url = f"https://api.telegram.org/bot{TOKEN}/{metodo}"
    try:
        r = requests.post(url, json=payload, timeout=20)
        return r.json()
    except: return None

# 2. BÚSQUEDA NACIONAL REAL (PORTAL DGCP)
def buscar_portal_gobierno():
    url_busqueda = "https://www.comprasdominicana.gob.do/portal/consultas/procesos/listado.aspx"
    keywords = ["Impermeabilización", "Lona Asfáltica", "Techo", "Filtración", "Remozamiento"]
    hallazgos = []
    for term in keywords:
        try:
            payload = {"txtSearch": term, "ddlProvincia": "0", "btnSearch": "Buscar"} 
            r = requests.post(url_busqueda, data=payload, timeout=15)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                filas = soup.find_all('tr', class_='grid-row') 
                for fila in filas:
                    cols = fila.find_all('td')
                    if len(cols) > 5:
                        codigo = cols[1].text.strip()
                        if codigo not in OBRAS_PROCESADAS:
                            hallazgos.append({
                                "codigo": codigo, 
                                "institucion": cols[2].text.strip(), 
                                "objeto": cols[3].text.strip(), 
                                "cierre": cols[5].text.strip(), 
                                "es_licitacion": "Licitación" in cols[4].text, 
                                "es_externo": False
                            })
        except: continue
    return hallazgos

# 3. INTELIGENCIA EXTERNA (REDES, FOROS, CONSTRUCTORAS)
def rastreo_inteligencia_total():
    hallazgos_externos = []
    plataformas = ["instagram.com", "facebook.com", "linkedin.com", "ingenieriaestrella.com", "constructora.com.do"]
    keywords = ["necesito impermeabilización", "subcontratación techo", "cotización lona asfáltica"]
    for plataforma in plataformas:
        for key in keywords:
            try:
                query = f"site:{plataforma} RD {key}"
                url_busqueda = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                r = requests.get(url_busqueda, headers=headers, timeout=10)
                if r.status_code == 200 and "No se han encontrado resultados" not in r.text:
                    id_ext = f"EXT-{random.randint(1000, 9999)}"
                    hallazgos_externos.append({
                        "fuente": plataforma.split('.')[0].upper(),
                        "objeto": f"Oportunidad detectada: {key}",
                        "institucion": "PROYECTO PRIVADO / REDES",
                        "codigo": id_ext,
                        "cierre": "URGENTE / CONTACTAR YA",
                        "es_licitacion": False,
                        "es_externo": True
                    })
            except: continue
    return hallazgos_externos

# 4. ENVÍO DE ALERTA CON SEMÁFORO FULL
def enviar_alerta_completa(obra):
    global OBRAS_PROCESADAS
    area_est = 2500 if "Nave" in obra['objeto'] or "Hospital" in obra['institucion'] or obra['es_externo'] else 700
    res = motor_idomi_avanzado(area_est)
    
    # --- SISTEMA DE SEMÁFORO COMPLETO ---
    if obra['es_externo']:
        tag = "💎 DIAMANTE | OPORTUNIDAD PRIVADA"
        nota = "🏗️ <b>ESTRATEGIA:</b> Detectado en redes/foros. Contactar por DM o llamada directa."
    elif "Emergencia" in obra['objeto'] or "Urgente" in obra['objeto']:
        tag = "🔥 FUEGO | CIERRE INMEDIATO"
        nota = "⚠️ <b>ESTRATEGIA:</b> Urgencia por filtración. Cierre en < 48h."
    elif area_est > 1500:
        tag = "🟠 NARANJA | PROYECTO GRAN ESCALA"
        nota = "🏗️ <b>ESTRATEGIA:</b> Gran volumen detectado nacionalmente. Preparar logística."
    elif obra['es_licitacion']:
        tag = "🟡 AMARILLO | LICITACIÓN NACIONAL"
        nota = "🏛️ <b>ESTRATEGIA:</b> Proceso formal DGCP. Usar costo de fábrica."
    else:
        tag = "🟢 VERDE | MANTENIMIENTO REGULAR"
        nota = "🏡 <b>ESTRATEGIA:</b> Residencial/Comercial. Enviar propuesta estándar."

    mensaje = (f"{tag}\n━━━━━━━━━━━━━━━━━━━━\n🏛️ <b>ORIGEN:</b> {obra['institucion']}\n🏗️ <b>REF:</b> <code>{obra['codigo']}</code>\n"
               f"📝 <b>OBJETO:</b> {obra['objeto']}\n📍 <b>COBERTURA:</b> NACIONAL RD\n━━━━━━━━━━━━━━━━━━━━\n"
               f"📐 <b>ÁREA:</b> {area_est} m²\n📦 <b>LOGÍSTICA:</b> {res['rollos']} Rollos + {res['primer']} Gal.\n"
               f"━━━━━━━━━━━━━━━━━━━━\n💰 <b>OFERTA IDOMI: RD$ {res['total']:,.0f}</b>\n📈 <b>GANANCIA: RD$ {res['neta']:,.0f}</b>\n"
               f"━━━━━━━━━━━━━━━━━━━━\n📅 <b>CIERRE:</b> {obra['cierre']}\n{nota}\n🛡️ <b>GARANTÍA: 15 AÑOS</b>")

    url_btn = f"https://www.google.com/search?q={urllib.parse.quote(obra['objeto'])}" if obra['es_externo'] else f"https://www.comprasdominicana.gob.do/portal/consultas/procesos/detalle.aspx?codigo={obra['codigo']}"
    botones = {"inline_keyboard": [[{"text": "📄 VER DETALLE REAL", "url": url_btn}], [{"text": "✉️ ENVIAR", "url": f"mailto:ventas@idomi.com.do?subject={obra['codigo']}"}]]}
    gestionar_telegram("sendMessage", {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML", "reply_markup": botones})
    OBRAS_PROCESADAS.add(obra['codigo'])

# 5. BUCLE MAESTRO CON LATIDO Y ANTI-BLOQUEO
def bucle_maestro():
    global ULTIMO_MSG_LATIDO
    gestionar_telegram("sendMessage", {"chat_id": CHAT_ID, "text": "<b>🛡️ HALCÓN v27.0 ACTIVADO</b>\nPatrullaje Nacional Total (Portal + Redes)", "parse_mode": "HTML"})
    ultimo_latido = time.time()
    
    while True:
        # Patrullaje Dual
        obras = buscar_portal_gobierno() + rastreo_inteligencia_total()
        for o in obras:
            enviar_alerta_completa(o)
            time.sleep(10)
            
        # Latido cada hora con limpieza
        if time.time() - ultimo_latido >= 3600:
            if ULTIMO_MSG_LATIDO: gestionar_telegram("deleteMessage", {"chat_id": CHAT_ID, "message_id": ULTIMO_MSG_LATIDO})
            ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
            res = gestionar_telegram("sendMessage", {"chat_id": CHAT_ID, "text": f"🛰️ <b>RADAR ACTIVO</b>\nRD: {ahora.strftime('%I:%M %p')}\nBuscando Obras Nacionales... ✅", "parse_mode": "HTML"})
            if res: ULTIMO_MSG_LATIDO = res.get('result', {}).get('message_id')
            ultimo_latido = time.time()

        # Pausa Inteligente (15-20 min)
        time.sleep(random.randint(900, 1200))

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle_maestro()
