import os
import requests
from dotenv import load_dotenv
import logging

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_API_URL = os.environ.get("GEMINI_API_URL")

def enhance_message(results):


    prompt = f"""
    You are a professional financial assistant. Here are the top S&P 500 stocks with their recent percentage changes:

    {results}

    Please provide output in two parts:
    1. **Stock summary:** List all the stocks exactly as given, with their percentage changes.
    2. **Actionable advice:** Give a short, clear summary and investment advice **relevant to these stocks as a 
group**. Focus only on trends, dominant performers, or patterns in the provided list. Keep the advice concise (3–5 
sentences). 

    Do not add generic or unrelated information.
    """

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json',
    }

    build_url = f'{GEMINI_API_URL}?key={GEMINI_API_KEY}'
    try:
        logging.info(f"Sending POST request to {build_url} with data: {data}")
        response = requests.post(build_url, headers=headers, json=data)
        # Process the response
        if response.status_code == 200:
            summary = response.json()
            try:
                return summary["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError, TypeError):
                return "summary error"
        else:
            summary = response.text
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print(f'Error exception: {e}')
    return summary


def enhance_message_advance(results):
    prompt = f"""
    You are a professional financial assistant creating a concise Telegram message.

    Here is the recent S&P 500 stock data:

    {results}

    Please format the output in two parts:

    1. 📊 Stock Summary:
       - Keep all the stocks exactly as given, grouped by Daily 📅, Weekly 📈, Monthly 📆, and Intersection 🔁.
       - Keep the emojis for up/down/neutral and the volume as in the input.
       - Make it easy to read on Telegram, each stock on a new line.

    2. 💡 Insight & Advice:
       - Provide a short, clear summary (3–5 sentences) about the stocks, focusing on the intersection first.
       - Mention trends, dominant performers, or patterns in the given list.
       - Keep the advice actionable and relevant **only to the stocks in this data**.
       - Do not add generic or unrelated information.

    Make sure the final message is compact and Telegram-friendly.
    """

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json',
    }

    build_url = f'{GEMINI_API_URL}?key={GEMINI_API_KEY}'
    try:
        logging.info(f"Sending POST request to {build_url} with data: {data}")
        response = requests.post(build_url, headers=headers, json=data)
        # Process the response
        if response.status_code == 200:
            summary = response.json()
            try:
                return summary["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError, TypeError):
                return "summary error"
        else:
            summary = response.text
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print(f'Error exception: {e}')
    return summary