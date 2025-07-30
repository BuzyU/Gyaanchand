import os
import requests

def query_llm(prompt):
    key = os.getenv("OPENROUTER_API_KEY")
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    body = {"model": "mistralai/mixtral-8x7b", "prompt": prompt}
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
    return response.json()
