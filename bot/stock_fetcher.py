import yfinance as yf
DEFAULT_TICKERS = ["AAPL", "MSFT", "GOOG", "TSLA", "NVDA", "AMZN", "META", "NFLX", "AMD", "INTC"]


def get_top_stocks(tickers=None, top_n=10):
    """
    Fetch stock data and return top movers by percentage change.

    :param tickers: list of stock symbols
    :param top_n: number of top movers to return
    :return: list of dicts: [{'symbol': 'AAPL', 'price': 174.2, 'change_pct': 2.5}, ...]
    """
    if tickers is None:
        tickers = DEFAULT_TICKERS

    data = yf.download(tickers, period="2d", interval="1d")  # last 2 days to calculate % change
    closes = data["Close"]
    top_stocks = []

    for t in tickers:
        try:
            today = closes[t].iloc[-1]
            yesterday = closes[t].iloc[-2]
            change_pct = ((today - yesterday) / yesterday) * 100
            top_stocks.append({
                "symbol": t,
                "price": round(today, 2),
                "change_pct": round(change_pct, 2)
            })
        except Exception as e:
            print(f"Error fetching {t}: {e}")
    top_stocks_sorted = sorted(top_stocks, key=lambda x: abs(x["change_pct"]), reverse=True)
    return top_stocks_sorted[:top_n]
