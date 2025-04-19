from config import get_credentials
from gmail_client import (
    build_gmail_service,
    list_latest_messages,
    read_message,
)


def main(event, context):
    creds = get_credentials()
    service = build_gmail_service(creds)

    print("📬 Checking for new messages...")
    new_ids = list_latest_messages(service, max_results=3)

    if new_ids:
        print(f"✅ Found {len(new_ids)} new message(s)")
        for msg_id in reversed(new_ids):
            read_message(service, msg_id)
    else:
        print("📭 No new messages.")

    return {
        "statusCode": 200,
        "body": "Poll complete"
    }


if __name__ == '__main__':
    main(None, None)
