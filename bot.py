import os
import time
from dotenv import load_dotenv
from binance.client import Client
import requests

# Cargar variables del archivo .env
load_dotenv()

# Configurar credenciales
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
CHAT_ID = os.getenv('CHAT_ID')

# URL para enviar mensajes por Telegram
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def enviar_mensaje_telegram(mensaje):
    """Envía un mensaje a Telegram"""
    try:
        datos = {
            'chat_id': CHAT_ID,
            'text': mensaje
        }
        requests.post(TELEGRAM_URL, data=datos)
        print(f"✓ Mensaje enviado: {mensaje}")
    except Exception as e:
        print(f"✗ Error al enviar mensaje: {e}")

def obtener_precio_actual(symbol='BTCUSDT'):
    """Obtiene el precio actual de un símbolo en Binance"""
    try:
        # Usar endpoint público de Binance (no necesita API key)
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        respuesta = requests.get(url)
        data = respuesta.json()
        return float(data['price'])
    except Exception as e:
        print(f"✗ Error al obtener precio: {e}")
        return None

def monitorear_precio():
    """Monitorea el precio y envía alertas"""
    precio_anterior = None
    
    print("🤖 Bot iniciado. Monitoreando precio de Bitcoin...")
    
    while True:
        try:
            precio_actual = obtener_precio_actual('BTCUSDT')
            
            if precio_actual is None:
                time.sleep(10)
                continue
            
            print(f"💰 Precio actual de BTC: ${precio_actual:,.2f}")
            
            if precio_anterior is not None:
                cambio_porcentaje = ((precio_actual - precio_anterior) / precio_anterior) * 100
                
                # Si el precio sube o baja más del 2%, envía alerta
                if abs(cambio_porcentaje) > 2:
                    tipo = "📈 SUBIDA" if cambio_porcentaje > 0 else "📉 BAJADA"
                    mensaje = f"{tipo}\n\nBTC: ${precio_actual:,.2f}\nCambio: {cambio_porcentaje:+.2f}%"
                    enviar_mensaje_telegram(mensaje)
            
            precio_anterior = precio_actual
            time.sleep(10)  # Espera 10 segundos antes de verificar de nuevo
            
        except Exception as e:
            print(f"✗ Error en el monitoreo: {e}")
            time.sleep(10)

if __name__ == "__main__":
    monitorear_precio()