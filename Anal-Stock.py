from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import yfinance as yf
import seaborn as sb
import pandas as pd
import numpy as np

# ==========================
# (NVDA) NVIDIA - King
# (META) META - AI + Advertising + Metaverse play
# (AVGO) Broadcom - AI chips + semiconductor + VMware
# (LLY) Eli Lilly - GLP-1 (Ozempic competitor) + pharma-AI
# (ASML) ASML Holding - EUV lithography monopoly

tickers = ['NVDA', 'META', 'AVGO', 'LLY', 'ASML']
waktu_berakhir = datetime.now()
waktu_mulai = waktu_berakhir - timedelta(days=5*365)

data_saham = pd.DataFrame()

for otak in tickers:
    try:
        # Download data for a single otak
        data = yf.download(otak, start=waktu_mulai, end=waktu_berakhir, progress=False) # progress=False to reduce output
        if not data.empty:
            if 'Adj Close' in data.columns:
                data_saham[otak] = data['Adj Close']
            elif 'Close' in data.columns:
                # Fallback to 'Close' price if 'Adj Close' is not available (e.g., if auto_adjust makes them identical)
                data_saham[otak] = data['Close']
                print(f"Warning: 'Adj Close' not found for {otak}, using 'Close' price.")
            else:
                print(f"Could not find 'Adj Close' or 'Close' data for {otak}.")
        else:
            print(f"No data downloaded for {otak}.")
    except Exception as e:
        print(f"Error fetching data for {otak}: {e}")

# Drop any rows with missing values that might occur if some dates are not present for all stocks
data_saham.dropna(inplace=True)

# 4. Tampilkan lima baris pertama dari DataFrame
print("Data harga saham historis (Adj Close) untuk 5 saham:")
print(data_saham.head())

print("\nInformasi DataFrame:\n")
data_saham.info()

# Plot
plt.figure(figsize=(18, 9))
data_saham.plot(ax=plt.gca())
plt.title('Harga saham selama 5 tahun', fontsize=16)
plt.xlabel('tahun')
plt.ylabel('Harga (USD)')
plt.legend(title='Saham')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ===========================================================
print("Informasi Ringkas DataFrame data_saham:")
data_saham.info()

print("\nStatistik Deskriptif DataFrame data_saham:")
print(data_saham.describe())

print("\nJumlah Nilai Hilang per Kolom di data_saham:")
print(data_saham.isnull().sum())

# ===========================================================