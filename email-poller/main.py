from config import get_credentials
from gmail_client import build_gmail_service, list_latest_messages, read_message

def main():
    #creds = get_credentials()
    #service = build_gmail_service(creds)
    #last_seen_id = None

    print("📬 Checking for new messages...")

    # TODO
    # new_ids = list_latest_messages(service, last_message_id=last_seen_id, max_results=3)
    new_ids = None

    if new_ids:
        print(f"✅ Found {len(new_ids)} new message(s)")
        #for msg_id in reversed(new_ids):
        #    read_message(service, msg_id)
        #last_seen_id = new_ids[0]
    else:
        print("📭 No new messages.")


if __name__ == '__main__':
    main()

