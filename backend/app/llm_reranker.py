import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-coder:6.7b"

def explain(query: str, code: str) -> str:
    prompt = f"""
Explain why this code matches the query.

Query:
{query}

Code:
{code}
"""
    r = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )
    return r.json()["response"].strip()
