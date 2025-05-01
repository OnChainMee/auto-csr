import boto3
import json
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
            "content": """You are a professional and empathetic customer service agent. 
            Always sound helpful, understanding, and clear.
            Do not use first-person language such as I, we, or me. Write in an impersonal, professional tone.
            """
        },
        {
            "role": "user",
            "content": """I want you to write a reply to a customer who needs help understanding how to return an item.
            Please explain that a printable shipping label is attached to the email you are writing them.
            Use HTML formatting in your response and output only the raw HTML. 
            Do not include markdown, triple backticks, or language tags.
            """
        }
    ],
    "temperature": 0.25,
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
        return response.json()["choices"][0]["message"]["content"]


if __name__ == '__main__':
    email_writer = EmailWriter()
    email_writer.write_customer_return_email()
