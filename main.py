import os, time, requests, datetime, random, urllib.parse, re
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread
from flask import Flask # Para mantener vivo el bot en Render Gratis

# --- CONFIGURACIÓN DE MANTENIMIENTO (KEEP ALIVE) ---
app = Flask('')

@app.route('/')
def home():
    return "🦅 HALCÓN IDOMI v30.2: Patrullando la Nación... ✅"

def run_flask():
    # Render usa el puerto 10000 por defecto para servicios web gratuitos
    app.run(host='0.0.0.0', port=10000)

# --- CONFIGURACIÓN DE CONTACTO ---
# Tu ID de chat de Telegram
CHAT_ID = "5324546877" 
TOKEN_TELEGRAM = "AQUÍ_TU_TOKEN_DE_BOTFATHER" # Reemplaza con tu token real

# --- IDENTIDAD Y SEGURIDAD (ANTI-BANEO) ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

# --- KEYWORDS DE COBERTURA TOTAL (Impermeabilización + Construcción) ---
KEYWORDS = [
    "impermeabilizacion", "manto asfaltico", "filtracion", "techos", 
    "sellado", "pintura elastomerica", "aislamiento termico", 
    "reparacion losa", "humedad", "goteras", "imprimacion",
    "IDOMI", "S.R.L.", "lona asfaltica", "mantenimiento naves", 
    "filtraciones industriales", "asfalto liquido"
]

FUENTES_EXT = ["facebook_groups_rd", "instagram_biz_rd", "clasificados_rd", "diario_libre"]
OBRAS_PROCESADAS = set()
ULTIMO_MSG_LATIDO = None

# 1. MOTOR DE CÁLCULO IDOMI (Realista y Rentable)
def motor_idomi_avanzado(area):
    costo_material = area * 450 
    mano_obra = area * 180 
    total = costo_material + mano_obra
    neta = total * 0.38 # 38% de ganancia neta estimada
    return {"total": total, "neta": neta}

# 2. PATRULLAJE CON "SIGILO" (Portal + Redes + Ingenieros)
def patrullaje_nacional(query):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        # Pausa aleatoria para que parezca una persona real navegando
        time.sleep(random.uniform(2, 5))
        # Aquí va tu lógica de scraping del portal y redes
        # Retorna una lista de dicts con: codigo, institucion, objeto, tel, email, ingeniero, cierre
        return [] 
    except:
        return []

# 3. EJECUCIÓN OMNIPRESENTE (Multihilo con Tiempo Límite)
def motor_de_busqueda_total():
    hallazgos = []
    # 15 hilos trabajando al mismo tiempo por toda la red
    with ThreadPoolExecutor(max_workers=15) as executor:
        futuros = {executor.submit(patrullaje_nacional, kw): kw for kw in KEYWORDS}
        futuros.update({executor.submit(patrullaje_nacional, f): f for f in FUENTES_EXT})
        
        try:
            # Si en 85 segundos no responde una fuente, la saltamos para no trabar el bot
            for futuro in as_completed(futuros, timeout=85):
                hallazgos.extend(futuro.result())
        except Exception:
            pass 
    return hallazgos

# 4. ENVÍO DE ALERTA CON SEMÁFORO (Datos Reales)
def enviar_alerta_integral(obra):
    global OBRAS_PROCESADAS
    if obra['codigo'] in OBRAS_PROCESADAS: return

    # Inteligencia de detección de área según tipo de edificio
    area_est = 2800 if any(x in obra['objeto'].lower() for x in ["nave", "hospital", "clinica", "escuela"]) else 750
    res = motor_idomi_avanzado(area_est)
    
    # --- SEMÁFOROS ESTRATÉGICOS ---
    obj = obra['objeto'].lower()
    if "emergencia" in obj or "urgente" in obj:
        tag, nota = "🔥 FUEGO | CIERRE INMEDIATO", "⚠️ <b>ATAQUE:</b> Filtración crítica detectada ahora."
    elif area_est >= 2000:
        tag, nota = "💎 DIAMANTE | PROYECTO ELITE", "💰 <b>ATAQUE:</b> Proyecto industrial de alta ganancia."
    elif "licitación" in obj:
        tag, nota = "🟡 AMARILLO | DGCP NACIONAL", "🏛️ <b>ATAQUE:</b> Proceso formal. Revisar pliegos."
    else:
        tag, nota = "🟢 VERDE | MANTENIMIENTO", "🔍 <b>ATAQUE:</b> Oportunidad estándar de servicio."

    mensaje = (
        f"{tag}\n━━━━━━━━━━━━━━━━━━━━\n"
        f"🏛️ <b>ORIGEN:</b> {obra['institucion']}\n"
        f"🏗️ <b>REF:</b> <code>{obra['codigo']}</code>\n"
        f"👷‍♂️ <b>ING./RESP:</b> {obra['ingeniero']}\n"
        f"📞 <b>TEL:</b> {obra['tel']}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 <b>OBJETO:</b> {obra['objeto']}\n"
        f"📐 <b>ÁREA:</b> {area_est} m² aprox.\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 <b>OFERTA IDOMI: RD$ {res['total']:,.0f}</b>\n"
        f"📈 <b>GANANCIA NETA: RD$ {res['neta']:,.0f}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ <b>GARANTÍA IDOMI: 15 AÑOS</b>\n"
        f"{nota}"
    )

    url_btn = f"https://www.comprasdominicana.gob.do/portal/consultas/procesos/detalle.aspx?codigo={obra['codigo']}"
    botones = {
        "inline_keyboard": [
            [{"text": "📄 VER EXPEDIENTE REAL", "url": url_btn}],
            [{"text": "📞 LLAMAR AL INGENIERO", "url": f"tel:{obra['tel']}"}]
        ]
    }
    
    # Envío a Telegram
    try:
        url_tg = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
        requests.post(url_tg, json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML", "reply_markup": botones}, timeout=10)
        OBRAS_PROCESADAS.add(obra['codigo'])
    except Exception as e:
        print(f"Error enviando a Telegram: {e}")

# 5. BUCLE MAESTRO (Inmortalidad en Render Gratis)
def bucle_principal():
    print(f"🛡️ HALCÓN v30.2 ACTIVADO | ID: {CHAT_ID} | RD PATRULLAJE")
    ultimo_latido = time.time()
    
    while True:
        try:
            # Escaneo de toda la nación
            obras = motor_de_busqueda_total()
            
            if obras:
                for o in obras:
                    enviar_alerta_integral(o)
                    time.sleep(random.uniform(5, 10)) # Pausa humana entre envíos
            
            # Mensaje de radar cada hora (Para que sepas que sigue vivo)
            if time.time() - ultimo_latido >= 3600:
                ahora = datetime.datetime.now()
                texto_latido = f"🛰️ <b>RADAR OMNI ACTIVO</b>\nRD: {ahora.strftime('%I:%M %p')}\nTodo normal en el patrullaje... ✅"
                requests.post(f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage", json={"chat_id": CHAT_ID, "text": texto_latido, "parse_mode": "HTML"})
                ultimo_latido = time.time()

            # PAUSA ANTI-BANEO (Simulación de descanso de usuario)
            espera = random.randint(300, 600) # De 5 a 10 minutos
            print(f"💤 Esperando {espera}s para el siguiente vuelo...")
            time.sleep(espera)

        except Exception as e:
            print(f"🚨 ERROR EN BUCLE: {e}. Reiniciando en 60s...")
            time.sleep(60)

if __name__ == "__main__":
    # PASO CRUCIAL PARA RENDER GRATIS: Levantar servidor web en un hilo aparte
    Thread(target=run_flask).start()
    
    # Iniciar el bot
    bucle_principal()
