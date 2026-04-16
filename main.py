import time
import requests
import schedule
from datetime import datetime

# --- CONFIGURACIÓN DE IDENTIDAD IDOMI ---
TOKEN_TELEGRAM = "7295779031:AAH8N_8F386N6Xv-9A-C65-Z2_6L78-D_A8"
CHAT_ID = "6159677329"

# Filtros estrictos para mantenimiento e impermeabilización
KEYWORDS = ["impermeabilizacion", "techo", "filtracion", "pintura", "manto"]
SIN_GARANTIA = ["-CM-", "-CD-"] # Compras Menores y Contrataciones Directas (Sin Póliza)

OBRAS_VISTAS = set()

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Error de red Telegram: {e}")

def calcular_analisis(monto):
    # Fórmula basada en el costo por m2 y margen de beneficio del 38%
    area = round(monto / 650)
    rollos = round(area / 9)
    pailas = round(area / 50)
    ganancia = round(monto * 0.38)
    return area, rollos, pailas, ganancia

def patrullar_portal_real():
    """
    CONEXIÓN DIRECTA A LA API DE DATOS ABIERTOS DGCP
    """
    print(f"[{datetime.now()}] Escaneando Base de Datos Oficial (DGCP)...")
    
    # URL oficial de procesos vigentes del gobierno dominicano
    API_URL = "https://api.dgcp.gob.do/api/v1/procesos/vigentes"
    
    try:
        response = requests.get(API_URL, timeout=45)
        if response.status_code != 200:
            return

        procesos = response.json().get('data', [])

        for p in procesos:
            referencia = p.get('referencia', '')
            
            # Evitar duplicados
            if referencia in OBRAS_VISTAS:
                continue

            descripcion = p.get('descripcion', '').lower()
            monto = float(p.get('monto_estimado', 0))
            fecha_cierre_str = p.get('fecha_cierre', '')

            # 1. Filtro de Rubro (Solo lo que tú haces)
            es_nuestro_negocio = any(k in descripcion for k in KEYWORDS)
            
            if es_nuestro_negocio:
                # 2. Filtro de Tiempo (Cierre en 5 días o menos)
                fecha_cierre = datetime.strptime(fecha_cierre_str, "%Y-%m-%d %H:%M")
                dias_restantes = (fecha_cierre - datetime.now()).days

                if 0 <= dias_restantes <= 5:
                    # 3. Clasificación de Garantía y Semáforo
                    es_sin_poliza = any(sigla in referencia for sigla in SIN_GARANTIA)
                    
                    area, rollos, pailas, ganancia = calcular_analisis(monto)
                    
                    if es_sin_poliza:
                        semaforo = "🔥 FUEGUITO (SIN PÓLIZA)"
                        garantia_txt = "❌ NO REQUIERE (Proceso Menor)"
                    elif monto >= 2000000:
                        semaforo = "💎 DIAMANTE (GRAN OBRA)"
                        garantia_txt = "⚠️ REQUIERE PÓLIZA (1%)"
                    else:
                        semaforo = "🟢 VERDE"
                        garantia_txt = "⚠️ REVISAR PLIEGO"

                    mensaje = (
                        f"{semaforo}\n"
                        f"🏗️ **Obra:** {p.get('descripcion')}\n"
                        f"🏢 **Entidad:** {p.get('entidad')}\n"
                        f"🆔 **Referencia:** `{referencia}`\n"
                        f"🛡️ **Garantía:** {garantia_txt}\n"
                        f"⏱️ **Cierre:** {fecha_cierre_str} ({dias_restantes} días)\n"
                        f"💰 **Presupuesto:** RD$ {monto:,.2f}\n"
                        f"---\n"
                        f"📊 **ANÁLISIS TÉCNICO IDOMI:**\n"
                        f"* Área Est.: {area} m²\n"
                        f"* Insumos: {rollos} Rollos / {pailas} Pailas\n"
                        f"* **Ganancia Est. (38%): RD$ {ganancia:,.2f}**\n\n"
                        f"🔗 [Link Directo al Portal](https://comprasdominicana.gob.do/procesos/{referencia})"
                    )
                    
                    enviar_telegram(mensaje)
                    OBRAS_VISTAS.add(referencia)

    except Exception as e:
        print(f"Error en patrullaje: {e}")

# Configurado para patrullar cada 15 minutos sin ser bloqueado
schedule.every(15).minutes.do(patrullar_portal_real)

if __name__ == "__main__":
    print("Mega-Halcón IDOMI V5.0 Iniciado...")
    enviar_telegram("🦅 **Mega-Halcón IDOMI V5.0 Online**\nConexión Real: API DGCP.\nSin datos inventados.")
    
    # Ejecución inicial para captar lo que hay abierto ahora mismo
    patrullar_portal_real()
    
    while True:
        schedule.run_pending()
        time.sleep(1)
