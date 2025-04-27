import boto3
import json

class EmailCategorizer:
    CATEGORIES = {
        "help with return",
        "customer complaint",
        "request for information",
        "spam"
    }
    ENDPOINT_NAME = "email-categorizer-endpoint"
    REGION = "us-east-1"
    PROMPT = """You are a customer service agent for an online clothing store. 
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

Email: {email_body}
Answer:
"""

    def __init__(self):
        self.sagemaker_runtime = boto3.client(
            "sagemaker-runtime", region_name=self.REGION)

    def categorize_email(self, email_body: str) -> str:
        email_body = json.dumps(email_body)[1:-1]
        prompt_text = self.PROMPT.format(email_body=email_body)

        response = self.sagemaker_runtime.invoke_endpoint(
            EndpointName=self.ENDPOINT_NAME,
            ContentType="application/json",
            Body=json.dumps({"inputs": prompt_text})
        )

        response_body = json.loads(response["Body"].read().decode())
        category = response_body[0]["generated_text"].strip()
        
        if category not in self.CATEGORIES:
            raise ValueError(f"Invalid category: {category}")

        return category
