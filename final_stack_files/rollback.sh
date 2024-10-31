#!/bin/bash

# Check if a stack name is provided
if [ $# -eq 0 ]; then
    echo "Please provide a stack name as an argument."
    echo "Usage: $0 <stack-name>"
    exit 1
fi

STACK_NAME=$1

# Delete all S3 buckets
echo "Deleting all S3 buckets..."
for i in $(aws s3 ls | cut -d" " -f3); do
    echo "Deleting bucket: $i"
    aws s3 rb s3://$i --force
done

# Rollback the CloudFormation stack
echo "Rolling back CloudFormation stack: $STACK_NAME"
aws cloudformation rollback-stack --stack-name $STACK_NAME

echo "Operations completed."