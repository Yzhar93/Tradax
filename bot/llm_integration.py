import os
import requests
from dotenv import load_dotenv
import json
load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_API_URL = os.environ.get("GEMINI_API_URL")

def enhance_message(results):
    prompt = f"""
    Analyze the following S&P 500 stock data and provide a concise summary with investment advice:
    
    {results}
    
    Please ensure the summary is short and includes actionable investment advice.
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
    return summary
