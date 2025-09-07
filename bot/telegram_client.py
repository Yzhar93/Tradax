import os
import requests


def send_telegram_message(message):
    """
    Send a message to a Telegram chat using a bot.

    Requires the environment variables:
    - TELEGRAM_BOT_TOKEN
    - TELEGRAM_CHAT_ID

    :param message: string, the message to send
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise ValueError("Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"  # optional: allows Markdown formatting
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise Exception(f"Failed to send message: {response.text}")

    return response.json()