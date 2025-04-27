#!/bin/sh
aws secretsmanager create-secret \
  --name GmailOAuthCredentials \
  --secret-binary fileb://credentials.json

aws secretsmanager create-secret \
  --name GmailOAuthToken \
  --secret-binary fileb://token.pickle
