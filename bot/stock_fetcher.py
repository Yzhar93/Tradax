import yfinance as yf
import pandas as pd


def get_sp500_tickers():
    url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv'
    df = pd.read_csv(url)
    sp500_symbols = df['Symbol'].tolist()
    return sp500_symbols

def get_top_stocks(top_n=10):
    tickers = get_sp500_tickers()
    data = yf.download(tickers, period="2d", interval="1d", group_by="ticker", progress=False)

    movers = []
    for t in tickers:
        try:
            closes = data[t]["Close"]
            today, yesterday = closes.iloc[-1], closes.iloc[-2]
            change_pct = ((today - yesterday) / yesterday) * 100
            movers.append({
                "symbol": t,
                "price": round(today, 2),
                "change_pct": round(change_pct, 2)
            })
        except Exception:
            pass

    movers_sorted = sorted(movers, key=lambda x: abs(x["change_pct"]), reverse=True)
    return movers_sorted[:top_n]