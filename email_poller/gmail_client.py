from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def build_gmail_service(creds):
    """
    Create and return the Gmail API service object.
    """
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred while building the Gmail service: {error}")
        return None

def list_latest_messages(service, last_message_id=None, max_results=5):
    """
    Fetch a list of the latest Gmail message IDs.
    Filters out messages seen in previous polls based on last_message_id.
    """
    try:
        results = service.users().messages().list(
            userId='me',
            maxResults=max_results,
            q='is:unread'
        ).execute()

        messages = results.get('messages', [])
        new_ids = []

        for msg in messages:
            if msg['id'] == last_message_id:
                break
            new_ids.append(msg['id'])

        return new_ids
    except HttpError as error:
        print(f"An error occurred while listing messages: {error}")
        return []

def read_message(service, msg_id):
    """
    Fetch and print details of a Gmail message given its ID.
    """
    try:
        message = service.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'
        ).execute()

        headers = message.get('payload', {}).get('headers', [])
        subject = _get_header(headers, 'Subject')
        sender = _get_header(headers, 'From')
        snippet = message.get('snippet', '')

        print(f"📧 Subject: {subject}")
        print(f"👤 From: {sender}")
        print(f"✂️ Snippet: {snippet}")
        print("-" * 40)

        return {
            'id': msg_id,
            'subject': subject,
            'from': sender,
            'snippet': snippet
        }

    except HttpError as error:
        print(f"An error occurred while reading message {msg_id}: {error}")
        return None

def _get_header(headers, name):
    """
    Helper to extract a header value from the headers list.
    """
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    return '(not found)'

def send_reply(service, msg_id, reply_body):
    """
    Send a reply to a Gmail message.
    """
    message = service.users().messages().get(userId='me', id=msg_id).execute()
    thread_id = message['threadId']

    reply_message = {
        'raw': reply_body,
        'threadId': thread_id
    }

    service.users().messages().send(userId='me', body=reply_message).execute()
    print(f"Replied to message ID: {msg_id}")
