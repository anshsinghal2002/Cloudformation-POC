# Check if a stack name is provided
if [ $# -eq 0 ]; then
    echo "Please provide a stack name as an argument."
    echo "Usage: $0 <stack-name>"
    exit 1
fi

STACK_NAME=$1
aws cloudformation deploy \
  --template-file final_stack_files/testpipeline.yaml \
  --stack-name $STACK_NAME \
  --capabilities CAPABILITY_IAM