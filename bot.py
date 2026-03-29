import yfinance as yf
import pandas as pd
import ta
import requests
import time
import os

# 🔑 VARIABLES
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def enviar_mensaje(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def analizar():
    data = yf.download("BTC-USD", period="1mo", interval="1h")

    close = data["Close"].squeeze()

    data["RSI"] = ta.momentum.RSIIndicator(close).rsi()
    data["EMA20"] = ta.trend.EMAIndicator(close, window=20).ema_indicator()
    data["EMA50"] = ta.trend.EMAIndicator(close, window=50).ema_indicator()

    data = data.dropna()

    rsi = data["RSI"].iloc[-1]
    ema20 = data["EMA20"].iloc[-1]
    ema50 = data["EMA50"].iloc[-1]

    if rsi < 30 and ema20 > ema50:
        señal = "🚀 COMPRA"
    elif rsi > 70 and ema20 < ema50:
        señal = "🔻 VENTA"
    else:
        señal = "⏸ ESPERAR"

    mensaje = f"""
📊 BTC

RSI: {round(rsi,2)}
EMA20: {round(ema20,2)}
EMA50: {round(ema50,2)}

Señal: {señal}
"""

    print(mensaje)
    enviar_mensaje(mensaje)

# 🔁 LOOP INFINITO
while True:
    analizar()
    time.sleep(3600)  # cada 1 hora