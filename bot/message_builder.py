def build_message(top_stocks, title="📈 Daily Stock Update"):
    """
    Build a formatted message for Telegram from top stocks data.

    :param top_stocks: list of dicts [{'symbol', 'price', 'change_pct'}, ...]
    :param title: optional title for the message
    :return: string ready to send
    """
    if not top_stocks:
        return f"{title}\n\nNo stock data available today."

    lines = [title, ""]
    for stock in top_stocks:
        symbol = stock["symbol"]
        price = stock["price"]
        change = stock["change_pct"]
        emoji = "🔺" if change > 0 else "🔻" if change < 0 else "⏺"
        lines.append(f"{emoji} {symbol}: ${price} ({change:+.2f}%)")

    message = "\n".join(lines)
    return message