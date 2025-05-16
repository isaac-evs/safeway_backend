#!/bin/bash

export DATABASE_URL=$(aws ssm get-parameter --name "/safeway-backend/DATABASE_URL" --with-decryption --query "Parameter.Value" --output text --region us-east-2)
export SECRET_KEY=$(aws ssm get-parameter --name "/safeway-backend/SECRET_KEY" --with-decryption --query "Parameter.Value" --output text --region us-east-2)

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
