import yfinance as yf
import pandas as pd


def get_sp500_tickers():
    url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv'
    df = pd.read_csv(url)
    sp500_symbols = df['Symbol'].tolist()
    return sp500_symbols

# def get_top_stocks(top_n=10):
#     tickers = get_sp500_tickers()
#     data = yf.download(tickers, period="2d", interval="1d", group_by="ticker", progress=False)
#
#     movers = []
#     for t in tickers:
#         try:
#             closes = data[t]["Close"]
#             today, yesterday = closes.iloc[-1], closes.iloc[-2]
#             change_pct = ((today - yesterday) / yesterday) * 100
#             movers.append({
#                 "symbol": t,
#                 "price": round(today, 2),
#                 "change_pct": round(change_pct, 2)
#             })
#         except Exception:
#             pass
#
#     movers_sorted = sorted(movers, key=lambda x: abs(x["change_pct"]), reverse=True)
#     return movers_sorted[:top_n]


# def get_top_stocks(top_n=10):
#     tickers = get_sp500_tickers()
#     try:
#         data = yf.download(tickers, period="2d", interval="1d", group_by="ticker", progress=False)
#     except Exception as e:
#         print(f"YF download failed: {e}")
#         return []
#
#     movers = []
#     for t in tickers:
#         if t not in data:
#             print(f"Ticker missing: {t}")
#             continue
#         try:
#             closes = data[t]["Close"]
#             today, yesterday = closes.iloc[-1], closes.iloc[-2]
#             change_pct = ((today - yesterday) / yesterday) * 100
#             movers.append({
#                 "symbol": t,
#                 "price": round(today, 2),
#                 "change_pct": round(change_pct, 2)
#             })
#         except Exception as e:
#             print(f"Failed to process {t}: {e}")
#             continue
#
#     movers_sorted = sorted(movers, key=lambda x: abs(x["change_pct"]), reverse=True)
#     return movers_sorted[:top_n]

def get_top_stocks(top_n=10):
    tickers = get_sp500_tickers()
    movers = []

    for t in tickers:
        t_yf = t.replace(".", "-")  # fix Yahoo tickers
        try:
            data = yf.download(t_yf, period="2d", interval="1d", group_by="ticker", progress=False)
            if data.empty:
                print(f"No data for {t}")
                continue
            closes = data["Close"]
            today, yesterday = closes.iloc[-1], closes.iloc[-2]
            change_pct = ((today - yesterday) / yesterday) * 100
            movers.append({
                "symbol": t,
                "price": round(today, 2),
                "change_pct": round(change_pct, 2)
            })
        except Exception as e:
            print(f"Failed {t}: {e}")
            continue

    movers_sorted = sorted(movers, key=lambda x: abs(x["change_pct"]), reverse=True)
    return movers_sorted[:top_n]
