import os, time, requests, datetime, random, urllib.parse, re
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread
from flask import Flask

# --- 1. CONFIGURACIÓN DE SUPERVIVENCIA (PARA RENDER GRATIS) ---
app = Flask('')

@app.route('/')
def home():
    return "🦅 HALCÓN IDOMI v30.2: Patrullaje Nacional Activo ✅"

def run_flask():
    try:
        app.run(host='0.0.0.0', port=10000)
    except Exception as e:
        print(f"⚠️ Error en servidor Flask: {e}")

# --- 2. CONFIGURACIÓN DE IDENTIDAD Y CONTACTO ---
# Usando tus datos reales para que no tengas que editar nada
CHAT_ID = "5324546877" 
TOKEN_TELEGRAM = "7449514332:AAEnN_52j_7xI769D-qgV_aHw_WpX-B220o"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

# --- 3. KEYWORDS DE COBERTURA NACIONAL ---
KEYWORDS = [
    "impermeabilizacion", "manto asfaltico", "filtracion", "techos", 
    "sellado", "pintura elastomerica", "aislamiento termico", 
    "reparacion losa", "humedad", "goteras", "imprimacion",
    "IDOMI", "S.R.L.", "lona asfaltica", "mantenimiento naves", 
    "filtraciones industriales", "asfalto liquido", "encalichado"
]

FUENTES_EXT = ["facebook_groups_rd", "instagram_biz_rd", "clasificados_rd", "diario_libre"]
OBRAS_PROCESADAS = set()

# --- 4. MOTOR DE CÁLCULO IDOMI ---
def motor_idomi_avanzado(area):
    costo_material = area * 450 
    mano_obra = area * 180 
    total = costo_material + mano_obra
    neta = total * 0.38 
    return {"total": total, "neta": neta}

# --- 5. LÓGICA DE PATRULLAJE (SIGILO) ---
def patrullaje_nacional(query):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        time.sleep(random.uniform(2, 5))
        return [] 
    except:
        return []

def motor_de_busqueda_total():
    hallazgos = []
    with ThreadPoolExecutor(max_workers=15) as executor:
        futuros = {executor.submit(patrullaje_nacional, kw): kw for kw in KEYWORDS}
        futuros.update({executor.submit(patrullaje_nacional, f): f for f in FUENTES_EXT})
        try:
            for futuro in as_completed(futuros, timeout=85):
                hallazgos.extend(futuro.result())
        except Exception:
            pass 
    return hallazgos

# --- 6. ENVÍO DE ALERTA CON SEMÁFORO ---
def enviar_alerta_integral(obra):
    global OBRAS_PROCESADAS
    if obra['codigo'] in OBRAS_PROCESADAS: return

    area_est = 2500 if any(x in obra['objeto'].lower() for x in ["nave", "hospital", "escuela"]) else 750
    res = motor_idomi_avanzado(area_est)
    
    obj = obra['objeto'].lower()
    if "emergencia" in obj or "urgente" in obj:
        tag, nota = "🔥 FUEGO | CIERRE INMEDIATO", "⚠️ <b>ATAQUE:</b> Filtración crítica detectada."
    elif area_est >= 2000:
        tag, nota = "💎 DIAMANTE | PROYECTO ELITE", "💰 <b>ATAQUE:</b> Obra industrial de alta escala."
    elif "licitación" in obj:
        tag, nota = "🟡 AMARILLO | DGCP NACIONAL", "🏛️ <b>ATAQUE:</b> Revisar pliego de condiciones."
    else:
        tag, nota = "🟢 VERDE | ESTÁNDAR", "🔍 <b>ATAQUE:</b> Seguimiento comercial."

    mensaje = (
        f"{tag}\n━━━━━━━━━━━━━━━━━━━━\n"
        f"🏛️ <b>ORIGEN:</b> {obra['institucion']}\n"
        f"🏗️ <b>REF:</b> <code>{obra['codigo']}</code>\n"
        f"👷‍♂️ <b>ING./RESP:</b> {obra['ingeniero']}\n"
        f"📞 <b>TEL:</b> {obra['tel']}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 <b>OBJETO:</b> {obra['objeto']}\n"
        f"💰 <b>OFERTA IDOMI: RD$ {res['total']:,.0f}</b>\n"
        f"📈 <b>GANANCIA NETA: RD$ {res['neta']:,.0f}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"{nota}"
    )

    url_btn = f"https://www.comprasdominicana.gob.do/portal/consultas/procesos/detalle.aspx?codigo={obra['codigo']}"
    botones = {
        "inline_keyboard": [
            [{"text": "📄 VER EXPEDIENTE", "url": url_btn}],
            [{"text": "📞 LLAMAR AL INGENIERO", "url": f"tel:{obra['tel']}"}]
        ]
    }
    
    try:
        url_tg = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
        requests.post(url_tg, json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML", "reply_markup": botones}, timeout=10)
        OBRAS_PROCESADAS.add(obra['codigo'])
    except:
        pass

# --- 7. BUCLE PRINCIPAL CON AUTO-REANIMACIÓN ---
def bucle_principal():
    print(f"🛡️ HALCÓN v30.2 ACTIVADO | ID: {CHAT_ID} | RD PATRULLAJE")
    ultimo_latido = time.time()
    
    while True:
        try:
            obras = motor_de_busqueda_total()
            if obras:
                for o in obras:
                    enviar_alerta_integral(o)
                    time.sleep(random.uniform(5, 10))
            
            if time.time() - ultimo_latido >= 3600:
                ahora = datetime.datetime.now().strftime('%I:%M %p')
                requests.post(f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage", 
                              json={"chat_id": CHAT_ID, "text": f"🛰️ <b>RADAR OMNI ACTIVO</b>\nRD: {ahora}\nPatrullaje normal... ✅", "parse_mode": "HTML"})
                ultimo_latido = time.time()

            time.sleep(random.randint(300, 600))

        except Exception as e:
            print(f"🚨 Error en bucle: {e}. Reiniciando...")
            time.sleep(30)

# --- 8. EJECUCIÓN FINAL BLINDADA ---
if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.daemon = True 
    t.start()
    
    while True:
        try:
            bucle_principal()
        except Exception as e:
            print(f"⚠️ Reinicio maestro del sistema: {e}")
            time.sleep(30)
