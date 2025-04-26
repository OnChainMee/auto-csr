#!/bin/sh
aws s3 cp test-email.json s3://auto-csr-inbound-email-bucket/emails/test-email-$(date +%Y%m%d-%H%M%S).json
# aws logs describe-log-groups
aws logs tail /aws/lambda/csr-agent --follow

