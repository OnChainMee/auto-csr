import boto3
import email
import os

ses = boto3.client('ses')

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    response = s3.get_object(Bucket=bucket, Key=key)
    raw_email = response['Body'].read().decode('utf-8')
    msg = email.message_from_string(raw_email)

    subject = msg['subject']
    sender = msg['from']
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = msg.get_payload(decode=True).decode()

    print(f"Email from: {sender}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")

    # Send reply
    reply_from = os.environ.get("REPLY_FROM_EMAIL", sender)
    try:
        ses.send_email(
            Source=reply_from,
            Destination={'ToAddresses': [sender]},
            Message={
                'Subject': {'Data': f"RE: {subject}"},
                'Body': {'Text': {'Data': "Thanks for your message! We received it."}}
            }
        )
    except Exception as e:
        print("Failed to send reply:", e)

    return {'statusCode': 200, 'body': 'Processed and replied'}
