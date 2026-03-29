import yfinance as yf
import pandas as pd
import ta
import requests
import time
import os

# 🔑 VARIABLES
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 🔒 Guarda última señal
ultima_senal = None

def enviar_mensaje(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def analizar():
    global ultima_senal
    try:
        time.sleep(5)

        data = yf.download("BTC-USD", period="1mo", interval="1h")

        if data.empty:
            print("⚠️ No hay datos, reintentando...")
            return

        close = data["Close"].squeeze()

        data["RSI"] = ta.momentum.RSIIndicator(close).rsi()
        data["EMA20"] = ta.trend.EMAIndicator(close, window=20).ema_indicator()
        data["EMA50"] = ta.trend.EMAIndicator(close, window=50).ema_indicator()

        data = data.dropna()

        if data.empty:
            print("⚠️ Datos insuficientes")
            return

        rsi = data["RSI"].iloc[-1]
        ema20 = data["EMA20"].iloc[-1]
        ema50 = data["EMA50"].iloc[-1]

        if rsi < 30 and ema20 > ema50:
            señal = "🚀 COMPRA"
        elif rsi > 70 and ema20 < ema50:
            señal = "🔻 VENTA"
        else:
            señal = "⏸ ESPERAR"

        if señal != ultima_senal:
            mensaje = f"""
📊 BTC

RSI: {round(rsi,2)}
EMA20: {round(ema20,2)}
EMA50: {round(ema50,2)}

Señal: {señal}
"""
            print(mensaje)
            enviar_mensaje(mensaje)
            ultima_senal = señal
        else:
            print("Sin cambios...")

    except Exception as e:
        print(f"❌ Error: {e}")

# 🔁 LOOP INFINITO
while True:
    analizar()
    time.sleep(1800)  # cada 30 min