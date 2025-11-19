import matplotlib.pyplot as plt
import yfinance as yf
import seaborn as sb
import pandas as pd
import numpy as np
import datetime
# ===========================================================



ticker_symbol = ['IBM', 'TLKM.JK', 'ADBE', 'TCEHY']
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days= 5 * 365)
stock_data_yf = pd.DataFrame()

# = =========================================================== exchange rate 1
# rates = ['IDRUSD=X', 'HKDUSD=X']
# tickers = yf.download(' '.join(rates))
# exchange_rates = []
# for i in ticker_symbol.tickers:
#     exchange_rates.append(ticker_symbol.ticker[i].history(start=start_date, end=end_date).Close)

# ex_df = pd.DataFrame(exchange_rates).T
# ex_df.columns = rates
# ex_df['USDUSD=X'] = 1.0

# assets = {'IBM': 'USD',
#           'ADBE':'USD',
#           'TLKM.JK':'IDR',
#           'TCEHY':'USD'}

# =========================================================== exchange rate 2
# fx_mapping = {
#     'USD': 'USDIRR=X',  # USD to IDR
#     'IDR': None,        # Sudah IDR, no konversi
#     'HKD': 'HKDIRR=X'   # HKD to IDR
# }

# # Mapping ticker ke mata uang (sesuaikan jika tambah ticker)
# currency_map = {
#     'IBM': 'USD',
#     'TLKM.JK': 'IDR',
#     'ADBE': 'USD',
#     'TCEHY': 'HKD'
# }

# fx_data = {}

# for ticker, currency in currency_map.items():
#     if currency != 'IDR':
#         try:
#             fx_ticker = fx_mapping[currency]
#             fx = yf.download(fx_ticker, start=start_date, end=end_date, progress=False)
#             if not fx.empty and 'Close' in fx.columns:
#                 fx_data[fx_ticker] = fx['Close']
#                 print(f"FX data downloaded for {currency}: {fx_ticker}")
#             else:
#                 print(f"Warning: FX data empty for {currency}")
#         except Exception as e:
#             print(f"Error fetching FX for {currency}: {e}")

# =========================================================== exchange rate 3
assets_currency = {
    'IBM': 'USD',
    'TLKM.JK': 'IDR',
    'ADBE': 'USD',
    'TCEHY': 'USD'
}
prices_raw = pd.DataFrame()

for ticker in ticker_symbol:
    data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
    if not data.empty:
        prices_raw[ticker] = data['Close']   # auto_adjust=True → Close sudah = Adj Close
    else:
        print(f"Gagal download {ticker}")

print("Download saham selesai\n")

# ================== DOWNLOAD KURS IDR → USD (hanya satu yang dibutuhkan) ==================
# IDRUSD=X = berapa USD yang didapat dari 1 IDR
idr_to_usd = yf.download('IDRUSD=X', start=start_date, end=end_date, progress=False)['Close']

# Forward-fill kalau ada hari libur
idr_to_usd = idr_to_usd.reindex(prices_raw.index).ffill().bfill()

# ================== KONVERSI SEMUA KE USD ==================
prices_usd = prices_raw.copy()

for ticker in ticker_symbol:
    currency = assets_currency.get(ticker, 'USD')
    
    if currency == 'USD':
        # sudah USD, tidak perlu apa-apa
        continue
    elif currency == 'IDR':
        # Konversi IDR → USD
        prices_usd[ticker] = prices_raw[ticker] * idr_to_usd
    else:
        print(f"Belum support konversi dari {currency} untuk {ticker}")

for ticker in ticker_symbol :
    try:
        data = yf.download(ticker, start = start_date, end = end_date, progress = False)
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
            print(f"Data ga ke kedownload untuk {ticker}")
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")

stock_data_yf.dropna(inplace=True)

# Lima baris pertama dari dataframe
print("Data harga saham historis (Adj Close) untuk 5 saham:")
print(stock_data_yf.head())

print("\nInformasi DataFrame:\n")
stock_data_yf.info()

# ===========================================================
plt.figure(figsize=(18, 9))
stock_data_yf.plot(ax=plt.gca())
plt.title('Historical Adjusted Close Prices for Selected Stocks')
plt.xlabel('Date')
plt.ylabel('Adjusted Close Price (USD)')
plt.legend(title='Ticker')
plt.grid(True)
plt.tight_layout()
plt.show()

print("Grafik harga saham historis telah ditampilkan.")






# ===========================================================
