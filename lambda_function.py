from Tradax.bot.stock_fetcher import get_top_stocks
from Tradax.bot.message_builder import build_message
from Tradax.bot.telegram_client import send_telegram_message
from Tradax.bot.llm_integration import enhance_message  # optional

def lambda_handler(event, context):
    stocks = get_top_stocks()
    msg = build_message(stocks)
    msg = enhance_message(msg)  # optional Gemini integration
    send_telegram_message(msg)
    return {"status": "success"}