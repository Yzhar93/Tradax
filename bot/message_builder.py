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


def format_section(title, stocks, change_key, vol_key):
    """Format a single section (daily/weekly/monthly) into text."""
    if not stocks:
        return f"\n📈 {title} Top Movers:\n• No data available."

    lines = [f"\n📈 {title} Top Movers:"]
    for s in stocks:
        symbol = s["symbol"]
        price = s["price"]
        change = s[change_key]
        vol = s[vol_key]
        emoji = "🔺" if change > 0 else "🔻" if change < 0 else "⏺"
        lines.append(f"{emoji} {symbol}: ${price} ({change:+.2f}%) | Vol: {vol:,}")
    return "\n".join(lines)


def build_message_advance(top_stocks_data, title="📊 S&P 500 Movers Summary"):
    """Build a formatted Telegram message from stock data dictionary."""
    if not top_stocks_data or not any(top_stocks_data.values()):
        return f"{title}\n\nNo stock data available."

    parts = [title]

    parts.append(format_section("Daily", top_stocks_data.get("daily", []), "daily_change", "daily_vol"))
    parts.append(format_section("Weekly", top_stocks_data.get("weekly", []), "weekly_change", "weekly_vol"))
    parts.append(format_section("Monthly", top_stocks_data.get("monthly", []), "monthly_change", "monthly_vol"))

    intersection = top_stocks_data.get("intersection", [])
    if intersection:
        parts.append(f"\n🔁 Intersection (Consistent Movers): {', '.join(intersection)}")
    else:
        parts.append("\n🔁 No overlapping movers across periods.")

    return "\n".join(parts)
