# auto-csr

_Proof of concept for agent AI customer service representative bot._

Maryville Universisty of St. Louis
COSC 643 - Ethics of Artificial Intelligence
Spring 2025

## Project Description

Providing customer service comes with a significant cost for many companies. This cost comes at a time when there is increasing pressure to reduce expenses to drive growth and profitability. At the same time, the expectations from consumers for high quality, around-the-clock assistance has grown (Carter, 2024). 

This project will demonstrate using agentic artificial intelligence (agentic AI) to automate customer service. By using agentic AI, companies can deliver high quality, personalized, and responsive customer service in a way that helps control expenses and scales. 

Agentic AI is the use of AI to create autonomous AI agents that are capable of independent action (AI agents). This form of AI itself depends on other AI such as machine learning and generative AI. Agentic AI differs from AI such as machine learning (which makes predictions or performs clustering) and generative AI (which generates content like text and images) in that it takes actions based on input. 

Acting based on input is similar to how human customer service representatives operate. Given a customer request (for instance, in a phone call, email, chat) the customer representative will take some action – collect more information, send a return shipping label, or provide store credit. 

This project will demonstrate how agentic AI can be used to both service customer requests as well as help human customer service representatives more effectively respond to customers.

## Project Plan 

Creating a sophisticated, full featured agentic AI customer service implementation would take resources (significantly) outside the time allotted for this class. However, the scope for the agent can be constrained so that the concept of the technology can be demonstrated and reveal the connection to ethical AI. 

To constrain the problem space, the agent will be an email-based agent that is capable of a fixed number of customer service tasks. Upon receiving an email, the AI agent will process the message to determine what action to take. The agent may augment the information contained in the email with other data, such as the user’s profile and purchase history. The available actions will be constrained to just a handful, such as replying for more information, replying and passing the issues on to a human representative, or replying and taking some direct action. 

Most of the intelligence from the agent will come from using a large language model (LLM) as the reasoning facility. The LLM will be provided with the support email text as input and possibly be augmented by other information (e.g., user profile retrieved via API call). The prompt for the LLM will contain the user’s message, any supporting data, and a list of actions available to the agent. The LLM will respond with whichever action it deems to be appropriate. 

The LLM will then be prompted to write a reply to the user. This reply will confirm the receipt of the user’s request and inform the user what action will be taken. If the required action needs more than just an email reply, the agent will do so (via API integration). 

This project will use Amazon Web Services for AI capabilities (such as for the LLM) and hosting for other required services. Any of the downstream services needed will be mocked so that the focus of the project is the creation of the AI agent. Email or a simple Web user interface will be used to demonstrate the customer service AI agent.

## Project Design

### Email Front-end

A Python lambda function polls Gmail for new mail. New mails are downloaded and
then stored in an S3 bucket to enable processing by the Auto CSR email
processor.

### Email Processor

The email processor reads emails saved to the S3 bucket and uses an LLM to
process them. The first round of processing categorizes the nature of the
email into one of the following categories.

- help with return
- customer complaint
- request for information
- spam / not relevant / no response

The categorization is done by the LLM given an a useful prompt ("as a
customer service representative..."), the email text, and the categories. The
output is the LLM's classification of the email.

## Quick Start

For a quick test of the system:

1. **Local setup**: Install dependencies and set up Gmail OAuth credentials
2. **Deploy infrastructure**: Deploy SageMaker endpoint and Lambda functions to AWS
3. **Configure secrets**: Store Gmail credentials and OpenAI API key in AWS Secrets Manager
4. **Test**: Send an email to your monitored Gmail account or use the test script to upload a test email to S3

```bash
# Test by uploading a test email directly to S3 (bypasses Gmail polling)
./csr_agent/post-test-email.sh
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- AWS Account with appropriate permissions
- Gmail account with API access enabled
- OpenAI API key (for email generation)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/OnChainMee/auto-csr
   cd auto-csr
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r dev-requirements.txt
   ```

3. **Set up Gmail OAuth credentials**
   
   You'll need to create OAuth credentials for Gmail API access:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API
   - Create OAuth 2.0 credentials (Desktop application type)
   - Download the credentials JSON file and save it as `email_poller/credentials.json`

4. **Set up environment variables**
   
   For local development, you can set:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export INBOUND_EMAIL_BUCKET="mocked-bucket"  # For local testing with moto
   ```

5. **Initialize Gmail OAuth token (first time only)**
   
   Run the email poller locally to initiate OAuth flow:
   ```bash
   cd email_poller
   python main.py
   ```
   
   This will open a browser window for authentication. After successful authentication, a `token.pickle` file will be created.

### Running Locally

#### Test Email Poller

The email poller can be run locally with mocked S3 storage:

```bash
cd email_poller
python main.py
```

This will:
- Use mocked S3 (via `moto`) instead of real AWS S3
- Check for new unread emails in Gmail
- Save email metadata to the mocked S3 bucket
- Print results to console

#### Test Email Categorizer

```bash
cd email_categorizer
python model_test.py
```

#### Test Email Writer

```bash
cd email_writer
python email_writer.py
```

### AWS Deployment

#### 1. Deploy Email Categorizer (SageMaker Endpoint)

The email categorizer uses AWS SageMaker with a HuggingFace model. Deploy it using CloudFormation:

```bash
aws cloudformation deploy \
  --template-file email_categorizer/template.yaml \
  --stack-name email-categorizer-stack \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1
```

Or use the GitHub Actions workflow (see `.github/workflows/deploy-email-categorizer.yaml`).

#### 2. Set up AWS Secrets Manager

Store your Gmail OAuth credentials and OpenAI API key in AWS Secrets Manager:

**Gmail OAuth Credentials:**
```bash
aws secretsmanager create-secret \
  --name GmailOAuthCredentials \
  --secret-binary fileb://email_poller/credentials.json
```

**Gmail OAuth Token:**
```bash
aws secretsmanager create-secret \
  --name GmailOAuthToken \
  --secret-binary fileb://email_poller/token.pickle
```

**OpenAI API Key:**
```bash
aws secretsmanager create-secret \
  --name openai/api_key \
  --secret-string '{"OPENAI_API_KEY":"your-api-key-here"}'
```

#### 3. Package and Deploy Lambda Functions

**Email Poller:**
```bash
# Package the Lambda function
zip -r email-poller.zip email_poller/ -x "*.pyc" "__pycache__/*"

# Upload to S3
aws s3 cp email-poller.zip s3://your-code-bucket/lambda/email-poller.zip

# Deploy using CloudFormation
aws cloudformation deploy \
  --template-file infra/email-poller-template.yaml \
  --stack-name email-poller-stack \
  --parameter-overrides \
    CodeBucket=your-code-bucket \
    CodeKey=lambda/email-poller.zip \
    InboundEmailBucket=auto-csr-inbound-email-bucket \
    PollInterval=10 \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1
```

**CSR Agent:**
```bash
# Package the Lambda function (includes all dependencies)
pip install -r requirements.txt -t .
zip -r csr-agent.zip . -x "*.pyc" "__pycache__/*" "*.git*" "infra/*" ".github/*"

# Upload to S3
aws s3 cp csr-agent.zip s3://your-code-bucket/lambda/csr-agent.zip

# Deploy using CloudFormation
aws cloudformation deploy \
  --template-file infra/auto-csr-template.yaml \
  --stack-name auto-csr-stack \
  --parameter-overrides \
    CodeBucket=your-code-bucket \
    CodeKey=lambda/csr-agent.zip \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1
```

**Important:** Make sure to configure the S3 bucket event notification to trigger the CSR Agent Lambda when new emails are uploaded:
- Bucket: `auto-csr-inbound-email-bucket`
- Prefix: `emails/`
- Event type: `s3:ObjectCreated:*`
- Destination: CSR Agent Lambda function

### How It Works

1. **Email Polling**: The Email Poller Lambda runs on a schedule (default: every 10 minutes) and checks Gmail for new unread emails.

2. **Email Storage**: When new emails are found, they're saved as JSON files to the S3 bucket (`auto-csr-inbound-email-bucket/emails/`).

3. **S3 Event Trigger**: When a new email file is uploaded to S3, it automatically triggers the CSR Agent Lambda function.

4. **Email Categorization**: The CSR Agent:
   - Downloads the email JSON from S3
   - Sends the email snippet to the SageMaker endpoint for categorization
   - Receives one of: "help with return", "customer complaint", "request for information", or "spam"

5. **Response Generation**: Based on the category:
   - **"help with return"**: Uses OpenAI API to generate a professional return assistance email and sends it via Gmail
   - **Other categories**: Currently logged (additional logic can be added)

6. **Email Sending**: Replies are sent back through Gmail API, properly threaded to the original conversation.

### Testing

You can test the system by:

1. **Sending a test email** to the Gmail account being monitored
   - Wait for the poller to pick it up (or manually invoke the Lambda)
   - Check CloudWatch logs to see the categorization and processing
   - Verify the reply in the Gmail inbox

2. **Direct S3 upload (bypasses Gmail polling)**
   ```bash
   # Upload a test email JSON file directly to S3
   ./csr_agent/post-test-email.sh
   
   # This will:
   # - Upload test-email.json to the S3 bucket
   # - Trigger the CSR Agent Lambda
   # - Stream CloudWatch logs to see the processing
   ```

3. **Manual Lambda invocation** (if deployed):
   ```bash
   # Invoke the email poller manually
   aws lambda invoke \
     --function-name email-poller-v2 \
     --region us-east-1 \
     response.json
   ```

For local testing with mocked S3, see `email_poller/main.py` which includes local execution logic.

### Architecture Components

- **email_poller/**: Lambda function that polls Gmail and saves emails to S3
- **csr_agent/**: Lambda function triggered by S3 events that processes emails
- **email_categorizer/**: SageMaker endpoint using FLAN-T5 for email classification
- **email_writer/**: Module using OpenAI API to generate professional email responses
- **infra/**: CloudFormation templates for AWS infrastructure deployment

### Troubleshooting

- **Gmail Authentication Issues**: Ensure `credentials.json` and `token.pickle` are correctly set up. Token expires after a period; refresh may be needed.
- **SageMaker Endpoint**: Ensure the endpoint is deployed and accessible. Check endpoint name matches `email-categorizer-endpoint` in code.
- **AWS Permissions**: Verify IAM roles have permissions for S3, Secrets Manager, SageMaker, and Lambda execution.
- **S3 Event Notifications**: Ensure the S3 bucket is configured to trigger the CSR Agent Lambda on object creation.

## Connection to Ethical AI

The agentic AI customer service agent will show how AI can be developed ethically and treat people with a sense of decency. Ethical treatment and decency will extend to both the users of the agentic AI agent and the human service agents that work alongside it. 

The AI agent will be designed to treat users with a sense of decency by acknowledging that users’ time is precious, and each user has a need that agent may be able to help with. To that end, the AI agent should be as helpful as possible. However, there may be many situations where the agent is unable to assist or uncertain what to do. In that case, the agent should collect and summarize all available information so that the inquiry can be handled by a human agent. 

The AI agent will disclose that it is a non-human entity so that users are aware that they are being serviced by AI. Furthermore, the users will always have an option to switch to a human agent for any reason, such as if they prefer interacting with a person or feel the AI agent is not meeting their needs. 

The goal of the AI agent is not to replace human customer service representatives, but to offload routine inquiries and make the human agents more efficient. For example, the AI agent can collect and summarize information so that the human agent can focus on solving the customer’s problem and spend less time hunting for data. This better together approach acknowledges the value of the human agent and has the potential to make their job more satisfying by helping customers with non-routine issues. 

This approach aligns with my personal ethical framework. First, this approach demonstrates honesty and transparency by informing users that they are being served by an AI agent. Also, users are given the choice to use AI or opt out. Instead of replacing humans (and their jobs), humans are enhanced by having AI in the system. 

## References

Carter, Rebekah. (2024, June 28). AI Customer Support: The Use Cases, Best Practices, & Ethics. CX Today. https://www.cxtoday.com/contact-center/ai-customer-support-the-use-cases-best-practices-ethics/


## Contact

If have any question contact [me](https://t.me/OnChainMee)
