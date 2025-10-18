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



def get_top_stocks_advance(top_n=10, intersect_n=20):
    tickers = get_sp500_tickers()
    data = yf.download(tickers, period="1mo", interval="1d", group_by="ticker", progress=False)

    daily_changes, weekly_changes, monthly_changes = [], [], []

    for t in tickers:
        try:
            df = data[t]
            if len(df) < 2:
                continue

            today = df["Close"].iloc[-1]
            yesterday = df["Close"].iloc[-2]
            week_ago = df["Close"].iloc[-6] if len(df) > 6 else df["Close"].iloc[0]
            month_ago = df["Close"].iloc[-22] if len(df) > 22 else df["Close"].iloc[0]

            # --- % changes ---
            daily_change = ((today - yesterday) / yesterday) * 100
            weekly_change = ((today - week_ago) / week_ago) * 100
            monthly_change = ((today - month_ago) / month_ago) * 100

            # --- volumes ---
            daily_vol = df["Volume"].iloc[-1]
            weekly_vol = df["Volume"].iloc[-5:].mean()
            monthly_vol = df["Volume"].iloc[-21:].mean()

            stock_data = {
                "symbol": t,
                "price": round(today, 2),
                "daily_change": round(daily_change, 2),
                "weekly_change": round(weekly_change, 2),
                "monthly_change": round(monthly_change, 2),
                "daily_vol": int(daily_vol),
                "weekly_vol": int(weekly_vol),
                "monthly_vol": int(monthly_vol)
            }

            daily_changes.append(stock_data)
            weekly_changes.append(stock_data)
            monthly_changes.append(stock_data)

        except Exception:
            continue

    # --- Sort by absolute change ---
    daily_sorted = sorted(daily_changes, key=lambda x: abs(x["daily_change"]), reverse=True)[:intersect_n]
    weekly_sorted = sorted(weekly_changes, key=lambda x: abs(x["weekly_change"]), reverse=True)[:intersect_n]
    monthly_sorted = sorted(monthly_changes, key=lambda x: abs(x["monthly_change"]), reverse=True)[:intersect_n]

    # --- Find intersection (stocks appearing in all three) ---
    daily_set = {x["symbol"] for x in daily_sorted}
    weekly_set = {x["symbol"] for x in weekly_sorted}
    monthly_set = {x["symbol"] for x in monthly_sorted}
    intersection = daily_set & weekly_set & monthly_set

    # --- Output ---
    print("\n📈 Top 10 Daily Movers:")
    for s in daily_sorted[:top_n]:
        print(f"{s['symbol']}: {s['daily_change']}% | Vol: {s['daily_vol']}")

    print("\n📊 Top 10 Weekly Movers:")
    for s in weekly_sorted[:top_n]:
        print(f"{s['symbol']}: {s['weekly_change']}% | Avg Vol: {s['weekly_vol']}")

    print("\n📅 Top 10 Monthly Movers:")
    for s in monthly_sorted[:top_n]:
        print(f"{s['symbol']}: {s['monthly_change']}% | Avg Vol: {s['monthly_vol']}")

    print("\n🔁 Intersection of All Periods:")
    print(intersection if intersection else "No overlapping top movers.")

    return {
        "daily": daily_sorted[:top_n],
        "weekly": weekly_sorted[:top_n],
        "monthly": monthly_sorted[:top_n],
        "intersection": list(intersection)
    }
