import os
import pickle
import boto3
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def load_secret_from_aws(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretBinary']

def save_secret_to_aws(secret_name, binary_data):
    client = boto3.client('secretsmanager')
    client.update_secret(
        SecretId=secret_name,
        SecretBinary=binary_data
    )

def get_credentials():
    creds = None

    # === LOCAL DEV: Load from local files if available ===
    if os.path.exists("token.pickle") and os.path.exists("credentials.json"):
        print("🔓 Loading Gmail credentials from local files...")
        with open("token.pickle", "rb") as token_file:
            creds = pickle.load(token_file)
    else:
        print("🔐 Loading Gmail credentials from AWS Secrets Manager...")
        creds_binary = load_secret_from_aws("GmailOAuthToken")
        creds = pickle.loads(creds_binary)

    # === Refresh if needed ===
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("🔄 Refreshed Gmail token")

            # === SAVE updated token ===
            if os.path.exists("token.pickle"):
                # LOCAL: Save to local file
                with open("token.pickle", "wb") as token_file:
                    pickle.dump(creds, token_file)
            else:
                # AWS: Save to Secrets Manager
                save_secret_to_aws("GmailOAuthToken", pickle.dumps(creds))
        else:
            raise Exception("❌ Missing or invalid Gmail credentials")

    return creds
