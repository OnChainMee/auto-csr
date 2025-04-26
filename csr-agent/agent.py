import json
import boto3

s3 = boto3.client('s3')

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

            # TODO: agent processing logic here

        except Exception as e:
            print(f"Error processing file {key}: {e}")

    return {"statusCode": 200}
