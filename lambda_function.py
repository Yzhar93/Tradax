from Tradax.bot import get_top_stocks
from Tradax.bot import build_message
from Tradax.bot import send_telegram_message
from Tradax.bot import enhance_message  # optional

def lambda_handler(event, context):
    stocks = get_top_stocks()
    msg = build_message(stocks)
    msg = enhance_message(msg)  # optional Gemini integration
    send_telegram_message(msg)
    return {"status": "success"}