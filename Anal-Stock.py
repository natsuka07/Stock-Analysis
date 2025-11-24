import matplotlib.pyplot as plt
import yfinance as yf
import seaborn as sb
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==========================
tickers = ['IBM', 'TLKM.JK', 'ADBE', 'TCEHY']
end_date = datetime.now()
start_date = end_date - timedelta(days=3*365)

# Download saham (adjusted price)
print("Downloading stock data...")
data = yf.download(tickers, start=start_date, end=end_date,
                  progress=False, auto_adjust=True)

if data.empty or 'Close' not in data.columns:
    raise ValueError("Gagal download data saham!")

prices = data['Close'].copy()   # ini sudah adjusted close

# Download kurs USD/IDR
print("Downloading USD/IDR exchange rate...")
raw = yf.download('IDR=X', start=start_date, end=end_date,
                  progress=False, auto_adjust=True)

if raw.empty:
    raise ValueError("Kurs IDR=X kosong!")

exchange_rate = raw['Close'].copy()
exchange_rate.name = 'USDIDR'
exchange_rate = 1 / exchange_rate   # IDR=X → USD/IDR

# Sesuaikan index & isi missing values
exchange_rate = exchange_rate.reindex(prices.index, method='nearest')
# atau lebih lembut:
exchange_rate = exchange_rate.reindex(prices.index).ffill().bfill()

# Gabungkan
df = prices.copy()
df['USDIDR'] = exchange_rate

# Konversi TLKM.JK dari IDR ke USD
df['TLKM.JK'] = df['TLKM.JK'] / df['USDIDR']

# Hapus kolom temporary
df = df.drop(columns=['USDIDR'])

# Final DataFrame
stock_data_usd = df

print("Sukses! Data 5 tahun (TLKM.JK sudah dalam USD):")
print(stock_data_usd.tail(10))

# Plot
plt.figure(figsize=(18, 9))
stock_data_usd.plot()
plt.title('5-Year Historical Stock Prices\n(IBM, TLKM.JK, ADBE, TCEHY) — TLKM.JK converted to USD', fontsize=16)
plt.xlabel('Tanggal')
plt.ylabel('Harga (USD)')
plt.legend(title='Saham')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
# ===========================================================
# ==========================
tickers = ['IBM', 'TLKM.JK', 'ADBE', 'TCEHY']
end_date = datetime.now()
start_date = end_date - timedelta(days=5*365)

# Download saham (adjusted price)
print("Downloading stock data...")
data = yf.download(tickers, start=start_date, end=end_date,
                  progress=False, auto_adjust=True)

if data.empty or 'Close' not in data.columns:
    raise ValueError("Gagal download data saham!")

prices = data['Close'].copy()   # ini sudah adjusted close

# Download kurs USD/IDR
print("Downloading USD/IDR exchange rate...")
raw = yf.download('IDR=X', start=start_date, end=end_date,
                  progress=False, auto_adjust=True)

if raw.empty:
    raise ValueError("Kurs IDR=X kosong!")

exchange_rate = raw['Close'].copy()
exchange_rate.name = 'USDIDR'
exchange_rate = 1 / exchange_rate   # IDR=X → USD/IDR

# Sesuaikan index & isi missing values
exchange_rate = exchange_rate.reindex(prices.index, method='nearest')
# atau lebih lembut:
exchange_rate = exchange_rate.reindex(prices.index).ffill().bfill()

# Gabungkan
df = prices.copy()
df['USDIDR'] = exchange_rate

# Konversi TLKM.JK dari IDR ke USD
df['TLKM.JK'] = df['TLKM.JK'] / df['USDIDR']

# Hapus kolom temporary
df = df.drop(columns=['USDIDR'])

# Final DataFrame
stock_data_usd = df

print("Sukses! Data 5 tahun (TLKM.JK sudah dalam USD):")
print(stock_data_usd.tail(10))

# Plot
plt.figure(figsize=(18, 9))
stock_data_usd.plot()
plt.title('5-Year Historical Stock Prices\n(IBM, TLKM.JK, ADBE, TCEHY) — TLKM.JK converted to USD', fontsize=16)
plt.xlabel('Tanggal')
plt.ylabel('Harga (USD)')
plt.legend(title='Saham')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ===========================================================
