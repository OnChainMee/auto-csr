#!/bin/sh
aws secretsmanager put-secret-value \
  --secret-id GmailOAuthToken \
  --secret-binary fileb://token.pickle
