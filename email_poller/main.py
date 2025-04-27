from email_poller.config import get_credentials
from email_poller.email_store import EmailStore
from email_poller.gmail_client import (
    build_gmail_service,
    list_latest_messages,
    read_message,
)
import os


def main(event, context):
    email_store = EmailStore(os.environ.get("INBOUND_EMAIL_BUCKET"))
    creds = get_credentials()
    service = build_gmail_service(creds)

    print("📬 Checking for new messages...")
    new_ids = list_latest_messages(service, max_results=3)

    if new_ids:
        print(f"✅ Found {len(new_ids)} new message(s)")
        for msg_id in reversed(new_ids):
            msg = read_message(service, msg_id)
            email_store.save_email_to_s3(msg)
    else:
        print("📭 No new messages.")

    return {
        "statusCode": 200,
        "body": "Poll complete"
    }


if __name__ == '__main__':
    print("Running locally, S3 will be mocked")
    os.environ["INBOUND_EMAIL_BUCKET"] = "mocked-bucket"
    from moto import mock_aws
    import boto3
    with mock_aws():
        s3 = boto3.client("s3")
        s3.create_bucket(Bucket="mocked-bucket")
        main(None, None)
