import yfinance as yf
import pandas as pd
import ta
import requests

# 🔑 CONFIGURACIÓN TELEGRAM
TOKEN = "8678597737:AAEv1JBHc5zW4pft7_xgAB5wOxtHP2N1BXI"
CHAT_ID = "5423327242"

def enviar_mensaje(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
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
    print("🚀 COMPRA")
elif rsi > 70 and ema20 < ema50:
    print("🔻 VENTA")
else:
    print("⏸ ESPERAR")

print("\nDatos actuales:")
print(f"RSI: {rsi}")
print(f"EMA20: {ema20}")
print(f"EMA50: {ema50}")
mensaje_final = f"""
📊 Análisis BTC

RSI: {round(rsi,2)}
EMA20: {round(ema20,2)}
EMA50: {round(ema50,2)}
"""

enviar_mensaje(mensaje_final)