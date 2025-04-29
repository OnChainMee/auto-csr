import boto3
import os
import requests


def get_api_key():
    secrets_client = boto3.client("secretsmanager")
    response = secrets_client.get_secret_value(SecretId="openai/api_key")
    secret = json.loads(response["SecretString"])
    return secret["OPENAI_API_KEY"]


OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY") or get_api_key()
OPEN_AI_API_URL = "https://api.openai.com/v1/chat/completions"
REQUEST_HADERS = {
    "Authorization": f"Bearer {OPEN_AI_API_KEY}",
    "Content-Type": "application/json",
}

data = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": "system",
            "content": "You are a professional and empathetic customer service agent. Always sound helpful, understanding, and clear. Guide the customer step-by-step through the return process."
        },
        {
            "role": "user",
            "content": "Hi, I received the wrong item. I would like to return it. How do I proceed?"
        }
    ],
    "temperature": 0.3,
    "max_tokens": 500,
    "top_p": 1.0
}

class EmailWriter:
    def __init__(self):
        pass
    
    def write_customer_return_email(self) -> str:
        response = requests.post(OPEN_AI_API_URL, headers=REQUEST_HADERS, json=data)

        if response.status_code == 200:
            print(response.json()["choices"][0]["message"]["content"])
        else:
            print(f"Error {response.status_code}: {response.text}")
        return ""


if __name__ == '__main__':
    email_writer = EmailWriter()
    email_writer.write_customer_return_email()
