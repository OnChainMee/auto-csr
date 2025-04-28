import requests
import os

api_key = os.getenv("OPENAI_API_KEY")  # or paste your key directly

url = "https://api.openai.com/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    models = response.json()["data"]
    for model in models:
        print(model["id"])
else:
    print(f"Error {response.status_code}: {response.text}")
