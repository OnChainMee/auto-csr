import boto3
import json

ENDPOINT_NAME = "email-categorizer-endpoint"
REGION = "us-east-1"

sagemaker_runtime = boto3.client("sagemaker-runtime", region_name=REGION)

prompt = """You are a customer service agent for an online clothing store. 
Classify each email into one of the following categories:
- help with return
- customer complaint
- request for information
- spam

Examples:

Email: I need to return a shirt that was too small.
Answer: help with return

Email: You sent me the wrong item and I need to send it back so you can send the correct thing.
Answer: help with return

Email: I'm frustrated with the lack of updates on my order.
Answer: customer complaint

Email: What size should I order if I'm usually a medium?
Answer: request for information

Email: Your site is not working.
Answer: customer complaint

Email: Forward this email to three friends to win a free iPhone!
Answer: spam

Email: Hi, I received the wrong item and would like to return it.
Answer:return

Email: Dearest catalog crap despensor, Snoop dogg.
Answer:
"""

response = sagemaker_runtime.invoke_endpoint(
    EndpointName=ENDPOINT_NAME,
    ContentType="application/json",
    Body=json.dumps({"inputs": prompt})
)

result = json.loads(response["Body"].read().decode())
print("Generated text:", result[0]["generated_text"])
print(result)
