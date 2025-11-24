import matplotlib.pyplot as plt
import yfinance as yf
import seaborn as sb
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==========================
# tickers = ['IBM', 'TLKM.JK', 'ADBE', 'TCEHY']
tickers = ['NVDA', 'META', 'AVGO', 'LLY', 'ASML']
end_date = datetime.now()
start_date = end_date - timedelta(days=3*365)

stock_data_yf = pd.DataFrame()

for ticker in tickers:
    try:
        # Download data for a single ticker
        data = yf.download(ticker, start=start_date, end=end_date, progress=False) # progress=False to reduce output
        if not data.empty:
            if 'Adj Close' in data.columns:
                stock_data_yf[ticker] = data['Adj Close']
            elif 'Close' in data.columns:
                # Fallback to 'Close' price if 'Adj Close' is not available (e.g., if auto_adjust makes them identical)
                stock_data_yf[ticker] = data['Close']
                print(f"Warning: 'Adj Close' not found for {ticker}, using 'Close' price.")
            else:
                print(f"Could not find 'Adj Close' or 'Close' data for {ticker}.")
        else:
            print(f"No data downloaded for {ticker}.")
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")

# Drop any rows with missing values that might occur if some dates are not present for all stocks
stock_data_yf.dropna(inplace=True)

# 4. Tampilkan lima baris pertama dari DataFrame
print("Data harga saham historis (Adj Close) untuk 5 saham:")
print(stock_data_yf.head())

print("\nInformasi DataFrame:\n")
stock_data_yf.info()

# Plot
plt.figure(figsize=(18, 9))
stock_data_yf.plot()
plt.title('5-Year Historical Stock Prices', fontsize=16)
plt.xlabel('Tanggal')
plt.ylabel('Harga (USD)')
plt.legend(title='Saham')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
# ===========================================================
# ===========================================================




