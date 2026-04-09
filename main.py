import os, time, requests, datetime, random, urllib.parse, re
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread

# --- CONFIGURACIÓN DE CONTACTO ---
# He colocado tu ID de chat aquí para que las alertas lleguen directo
CHAT_ID = "5324546877" 

# --- IDENTIDAD Y SEGURIDAD (ANTI-BANEO NACIONAL) ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"
]

# --- KEYWORDS DE COBERTURA TOTAL (Construcción + Impermeabilización) ---
KEYWORDS = [
    "impermeabilizacion", "manto asfaltico", "filtracion", "techos", 
    "sellado", "pintura elastomerica", "aislamiento termico", 
    "reparacion losa", "humedad", "goteras", "imprimacion",
    "IDOMI", "S.R.L.", "lona asfaltica", "encalichado", "hormigon armado",
    "remodelacion", "mantenimiento de naves", "pintura de edificios"
]

# Fuentes que cubren toda la nación
FUENTES_EXT = ["facebook_groups_rd", "instagram_reels_eng", "linkedin_jobs_rd", "listin_diario_clasificados", "diario_libre_obras"]

OBRAS_PROCESADAS = set()
ULTIMO_MSG_LATIDO = None

# 1. MOTOR DE CÁLCULO IDOMI (Ajustado para obras nacionales)
def motor_idomi_avanzado(area):
    # Estimación de costos reales en RD
    costo_material = area * 450 
    mano_obra = area * 180 
    total = costo_material + mano_obra
    neta = total * 0.38 # 38% de ganancia para IDOMI
    return {"total": total, "neta": neta}

# 2. PATRULLAJE OMNIPRESENTE (Portal + Redes + Todo RD)
def buscar_en_fuentes_nacionales(criterio):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        # Simulamos una pausa de navegación humana
        time.sleep(random.uniform(2, 4))
        # Aquí va tu lógica de scraping que recorre el país
        return [] 
    except: return []

# 3. EJECUCIÓN MULTIHILO TURBO (Todo al mismo tiempo)
def patrullaje_total_blindado():
    hallazgos = []
    # 15 hilos trabajando en paralelo por todo el internet dominicano
    with ThreadPoolExecutor(max_workers=15) as executor:
        # Buscamos por palabras clave y por fuentes externas simultáneamente
        futuros = {executor.submit(buscar_en_fuentes_nacionales, kw): kw for kw in KEYWORDS}
        futuros.update({executor.submit(buscar_en_fuentes_nacionales, f): f for f in FUENTES_EXT})
        
        try:
            # Tiempo límite de 90 segundos para evitar que el bot se "congele"
            for futuro in as_completed(futuros, timeout=90):
                hallazgos.extend(futuro.result())
        except Exception:
            pass # Si una fuente falla, las demás siguen
            
    return hallazgos

# 4. ALERTA CON SEMÁFORO MAESTRO (Estrategia de Ataque)
def enviar_alerta_completa(obra):
    global OBRAS_PROCESADAS
    if obra['codigo'] in OBRAS_PROCESADAS: return

    # Inteligencia de área: Naves y Hospitales suelen ser > 2000m2
    area_est = 2500 if any(x in obra['objeto'].lower() for x in ["nave", "hospital", "escuela"]) else 700
    res = motor_idomi_avanzado(area_est)
    
    # --- LÓGICA DE SEMÁFORO ---
    obj = obra['objeto'].lower()
    if "emergencia" in obj or "urgente" in obj:
        tag, nota = "🔥 FUEGO | CIERRE INMEDIATO", "🆘 <b>ATAQUE:</b> Filtración crítica detectada."
    elif area_est >= 2000:
        tag, nota = "💎 DIAMANTE | PROYECTO ELITE", "💰 <b>ATAQUE:</b> Alta rentabilidad para IDOMI."
    elif "licitación" in obj:
        tag, nota = "🟡 AMARILLO | PROCESO DGCP", "🏛️ <b>ATAQUE:</b> Licitación formal nacional."
    else:
        tag, nota = "🟢 VERDE | MANTENIMIENTO", "🔍 <b>ATAQUE:</b> Seguimiento comercial estándar."

    mensaje = (
        f"{tag}\n━━━━━━━━━━━━━━━━━━━━\n"
        f"🏛️ <b>INSTITUCIÓN:</b> {obra['institucion']}\n"
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

    # Botones de acción rápida
    url_btn = f"https://www.comprasdominicana.gob.do/portal/consultas/procesos/detalle.aspx?codigo={obra['codigo']}"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "📄 EXPEDIENTE", "url": url_btn}],
                [{"text": "📞 LLAMAR AL INGENIERO", "url": f"tel:{obra['tel']}"}]
            ]
        }
    }
    
    # Envío real a Telegram
    requests.post(f"https://api.telegram.org/botTU_TOKEN_BOT/sendMessage", json=payload)
    OBRAS_PROCESADAS.add(obra['codigo'])

# 5. BUCLE INMORTAL (Patrullaje Nacional 24/7)
def bucle_maestro():
    print(f"🛡️ HALCÓN v30.2 ACTIVADO | ID: {CHAT_ID} | COBERTURA NACIONAL")
    ultimo_latido = time.time()
    
    while True:
        try:
            obras = patrullaje_total_blindado()
            if obras:
                for o in obras:
                    enviar_alerta_completa(o)
                    time.sleep(random.uniform(3, 6)) # Pausa humana
            
            # Latido cada hora (Radar activo)
            if time.time() - ultimo_latido >= 3600:
                print(f"🛰️ RADAR OMNI ACTIVO: {datetime.datetime.now().strftime('%I:%M %p')}")
                ultimo_latido = time.time()

            # PAUSA ANTI-BANEO (Entre 5 y 10 minutos)
            time.sleep(random.randint(300, 600))

        except Exception as e:
            print(f"🚨 REINICIANDO MOTOR: {e}")
            time.sleep(60)

if __name__ == "__main__":
    bucle_maestro()
