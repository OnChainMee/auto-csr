import json
import boto3
from email_categorizer.email_categorizer import EmailCategorizer
from email_writer.email_writer import EmailWriter
from email_poller.config import get_credentials
from email_poller.gmail_client import (
    build_gmail_service,
    send_reply
)

s3 = boto3.client('s3')
email_writer = EmailWriter()


def new_email(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(f"New file uploaded: s3://{bucket}/{key}")

        try:
            # Download the JSON file from S3
            response = s3.get_object(Bucket=bucket, Key=key)
            content = response['Body'].read().decode('utf-8')  # read bytes and decode to string
            data = json.loads(content)  # parse JSON

            # Now 'data' is a Python dictionary
            print("Parsed JSON content:")
            print(json.dumps(data, indent=2))

            email_category = categorize_email(data['snippet'])
            print(f"Email category: {email_category}")
            process_email(email_category, data['snippet'])
        except Exception as e:
            print(f"Error processing file {key}: {e}")

    return {"statusCode": 200}


def categorize_email(email_body: str) -> str:
    email_categorizer = EmailCategorizer()
    return email_categorizer.categorize_email(email_body)


def process_email(email_category: str, email_body: str, msg_id: str) -> None:
    match email_category:
        case "help with return":
            email_response = email_writer.write_customer_return_email()
            print("Email response:")
            print(email_response)
            gmail_service = build_gmail_service(get_credentials())
            send_reply(gmail_service, msg_id, email_response)
            return
        case "customer complaint":
            return
        case "request for information":
            return
        case "spam":
            return
