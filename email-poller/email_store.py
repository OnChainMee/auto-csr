import json
import boto3
from botocore.exceptions import ClientError


class EmailStore:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    def save_email_to_s3(self, email_data):
        message_id = email_data.get("id")
        if not message_id:
            raise ValueError("Email data must include an 'id' field.")

        key = f"emails/{message_id}.json"

        # Check if object already exists
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            print(f"🟡 Email {message_id} already exists in S3 — skipping.")
            return False  # Already exists
        except ClientError as e:
            if e.response['Error']['Code'] != '404':
                raise  # Some other error (not just missing file)

        # Save to S3
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=json.dumps(email_data),
            ContentType="application/json"
        )
        print(f"✅ Saved email {message_id} to S3")
        return True
