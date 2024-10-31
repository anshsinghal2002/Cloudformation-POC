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

# Attempt to delete the CloudFormation stack
echo "Deleting CloudFormation stack: $STACK_NAME"
aws cloudformation delete-stack --stack-name $STACK_NAME

# Wait for the stack deletion to complete
echo "Waiting for stack deletion to complete..."
aws cloudformation wait stack-delete-complete --stack-name $STACK_NAME

# If the stack still exists, attempt to delete it with --retain-resources
if aws cloudformation describe-stacks --stack-name $STACK_NAME 2>&1 | grep -q 'does not exist'; then
    echo "Stack deleted successfully."
else
    echo "Stack deletion failed. Attempting to delete with --retain-resources..."
    aws cloudformation delete-stack --stack-name $STACK_NAME --retain-resources $(aws cloudformation list-stack-resources --stack-name $STACK_NAME --query "StackResourceSummaries[*].LogicalResourceId" --output text)
    
    # Wait for the second deletion attempt to complete
    echo "Waiting for second stack deletion attempt to complete..."
    aws cloudformation wait stack-delete-complete --stack-name $STACK_NAME
fi

echo "Operations completed."