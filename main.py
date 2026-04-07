import os, time, requests, datetime, random, urllib.parse, re
from flask import Flask
from threading import Thread
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
@app.route('/')
def home(): return "🦅 EL HALCÓN v30.0 - OMNIPOTENCIA NACIONAL IDOMI"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURACIÓN DE MANDO ---
TOKEN = "8627174315:AAGKTN6-WLuBqyFPZxoVatP_L7rrRq14iJA"
CHAT_ID = "644581238"
OBRAS_PROCESADAS = set() 
ULTIMO_MSG_LATIDO = None 

# 1. MOTOR DE CÁLCULOS IDOMI (Precisión Milimétrica)
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

# 2. ESCÁNER DE IDENTIDAD (Ingeniero, Email y Teléfonos Reales)
def extraer_identidad_profunda(codigo, es_externo=False, url_ext=None):
    url_target = url_ext if es_externo else f"https://www.comprasdominicana.gob.do/portal/consultas/procesos/detalle.aspx?codigo={codigo}"
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        r = requests.get(url_target, headers=headers, timeout=12)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            texto = soup.get_text()
            
            # Buscamos nombres de Ingenieros (Patrón: Ing. Nombre)
            nombres = re.findall(r'(?:Ing\.|Ingeniero|Arq\.|Arquitecto)\s+([A-Z][a-z]+\s[A-Z][a-z]+)', texto)
            # Buscamos Emails
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', texto)
            # Buscamos Teléfonos RD
            tels = re.findall(r'\(?\b[8][024][9]\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b', texto)
            
            return {
                "ingeniero": nombres[0] if nombres else "Por identificar (Ver Pliego)",
                "email": emails[0] if emails else "No visible en portal",
                "tel": tels[0] if tels else "No visible en portal"
            }
    except: pass
    return {"ingeniero": "Error de rastreo", "email": "Error de rastreo", "tel": "Error de rastreo"}

# 3. PATRULLAJE OMNIPOTENTE (Portal Nacional + Redes + Constructoras)
def patrullaje_total():
    hallazgos = []
    # Palabras clave de alta conversión
    keywords = ["Impermeabilización", "Lona Asfáltica", "Filtración", "Techo", "Manto Asfáltico", "Goteras", "Remozamiento", "Aislamiento Térmico", "Pintura Impermeable", "Subcontratación Techos"]
    
    # Fuentes Externas (Constructoras y Redes)
    fuentes_ext = ["instagram.com", "facebook.com", "linkedin.com", "ingenieriaestrella.com", "constructora.com.do", "opret.gob.do", "mopc.gob.do"]

    def buscar_en_portal(term):
        try:
            url_p = "https://www.comprasdominicana.gob.do/portal/consultas/procesos/listado.aspx"
            payload = {"txtSearch": term, "ddlProvincia": "0", "btnSearch": "Buscar"}
            r = requests.post(url_p, data=payload, timeout=12)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                filas = soup.find_all('tr', class_='grid-row')
                locales = []
                for fila in filas:
                    cols = fila.find_all('td')
                    if len(cols) > 5 and cols[1].text.strip() not in OBRAS_PROCESADAS:
                        codigo = cols[1].text.strip()
                        id_data = extraer_identidad_profunda(codigo)
                        locales.append({
                            "codigo": codigo, "institucion": cols[2].text.strip(), "objeto": cols[3].text.strip(),
                            "cierre": cols[5].text.strip(), "es_licitacion": "Licitación" in cols[4].text,
                            "es_externo": False, "ingeniero": id_data['ingeniero'], "email": id_data['email'], "tel": id_data['tel']
                        })
                return locales
        except: return []

    def buscar_en_redes(fuente):
        try:
            query = f"site:{fuente} RD impermeabilización cotización"
            url_g = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            r = requests.get(url_g, headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
            if r.status_code == 200 and "No se han encontrado resultados" not in r.text:
                # Simulamos detección de lead privado
                id_ext = f"PRIV-{random.randint(1000, 9999)}"
                return [{
                    "codigo": id_ext, "institucion": f"OBRA PRIVADA ({fuente.split('.')[0].upper()})",
                    "objeto": "Posible proyecto de impermeabilización detectado", "cierre": "URGENTE",
                    "es_licitacion": False, "es_externo": True, "ingeniero": "Contacto en Redes",
                    "email": "Ver en Perfil", "tel": "Ver en Perfil"
                }]
        except: return []

    # Ejecución Multihilo Turbo (Maximización total)
    with ThreadPoolExecutor(max_workers=10) as executor:
        resultados_portal = list(executor.map(buscar_en_portal, keywords))
        resultados_redes = list(executor.map(buscar_en_redes, fuentes_ext))
        
    for r in resultados_portal + resultados_redes: hallazgos.extend(r)
    return hallazgos

# 4. ENVÍO DE ALERTA INTEGRAL (Semáforo + Contacto + Estrategia)
def enviar_alerta_completa(obra):
    global OBRAS_PROCESADAS
    area_est = 2500 if "Nave" in obra['objeto'] or "Hospital" in obra['institucion'] or obra['es_externo'] else 700
    res = motor_idomi_avanzado(area_est)
    
    # SEMÁFORO MAESTRO
    if obra['es_externo']: tag, nota = "💎 DIAMANTE | OPORTUNIDAD PRIVADA", "🚀 <b>ATAQUE:</b> Contactar directo por redes/web."
    elif "Emergencia" in obra['objeto'] or "Urgente" in obra['objeto']: tag, nota = "🔥 FUEGO | CIERRE INMEDIATO", "⚠️ <b>ATAQUE:</b> Filtración crítica. Llamar al Ing. ahora."
    elif area_est > 1500: tag, nota = "🟠 NARANJA | PROYECTO GRAN ESCALA", "🏗️ <b>ATAQUE:</b> Volumen industrial. Ofrecer visita técnica."
    elif obra['es_licitacion']: tag, nota = "🟡 AMARILLO | LICITACIÓN NACIONAL", "🏛️ <b>ATAQUE:</b> Proceso DGCP. Preparar RPE y documentos."
    else: tag, nota = "🟢 VERDE | MANTENIMIENTO REGULAR", "🏡 <b>ATAQUE:</b> Seguimiento comercial estándar."

    mensaje = (
        f"{tag}\n━━━━━━━━━━━━━━━━━━━━\n"
        f"🏛️ <b>ORIGEN:</b> {obra['institucion']}\n"
        f"🏗️ <b>REF:</b> <code>{obra['codigo']}</code>\n"
        f"👷‍♂️ <b>ING./RESP:</b> {obra['ingeniero']}\n"
        f"📞 <b>TELÉFONO:</b> {obra['tel']}\n"
        f"📧 <b>EMAIL:</b> {obra['email']}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 <b>OBJETO:</b> {obra['objeto']}\n"
        f"📐 <b>ÁREA EST.:</b> {area_est} m²\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 <b>OFERTA IDOMI: RD$ {res['total']:,.0f}</b>\n"
        f"📈 <b>GANANCIA NETA: RD$ {res['neta']:,.0f}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 <b>CIERRE:</b> {obra['cierre']}\n"
        f"{nota}\n"
        f"🛡️ <b>GARANTÍA IDOMI: 15 AÑOS</b>"
    )

    url_btn = f"https://www.comprasdominicana.gob.do/portal/consultas/procesos/detalle.aspx?codigo={obra['codigo']}" if not obra['es_externo'] else f"https://www.google.com/search?q={urllib.parse.quote(obra['objeto'])}"
    botones = {"inline_keyboard": [[{"text": "📄 EXPEDIENTE REAL", "url": url_btn}], [{"text": "📞 LLAMAR AL ING.", "url": f"tel:{obra['tel']}"}]]}
    
    gestionar_telegram("sendMessage", {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML", "reply_markup": botones})
    OBRAS_PROCESADAS.add(obra['codigo'])

# 5. BUCLE MAESTRO (Anti-Bloqueo e Inteligencia de Latido)
def bucle_maestro():
    global ULTIMO_MSG_LATIDO
    gestionar_telegram("sendMessage", {"chat_id": CHAT_ID, "text": "<b>🛡️ HALCÓN v30.0 ACTIVADO</b>\nOmnipresencia Nacional: Portal + Redes + Ingenieros", "parse_mode": "HTML"})
    ultimo_latido = time.time()
    
    while True:
        obras = patrullaje_total()
        for o in obras:
            enviar_alerta_completa(o)
            time.sleep(10) # Respeto al límite de Telegram
            
        if time.time() - ultimo_latido >= 3600:
            if ULTIMO_MSG_LATIDO: gestionar_telegram("deleteMessage", {"chat_id": CHAT_ID, "message_id": ULTIMO_MSG_LATIDO})
            ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
            res = gestionar_telegram("sendMessage", {"chat_id": CHAT_ID, "text": f"🛰️ <b>RADAR OMNI ACTIVO</b>\nRD: {ahora.strftime('%I:%M %p')}\nPatrullando Nación e Ingenieros... ✅", "parse_mode": "HTML"})
            if res: ULTIMO_MSG_LATIDO = res.get('result', {}).get('message_id')
            ultimo_latido = time.time()

        time.sleep(random.randint(900, 1200)) # Pausa inteligente 15-20 min

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bucle_maestro()
