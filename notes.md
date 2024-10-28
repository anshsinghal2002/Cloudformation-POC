# CloudFormation POC

## Simplest Use Case

### Spinnning up an S3 Bucket


```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Simple CloudFormation template to create an S3 bucket

Resources:
  MyS3Bucket:
    Type: 'AWS::S3::Bucket'
    Properties:
      AccessControl: Private
      VersioningConfiguration:
        Status: Enabled
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

Outputs:
  BucketName:
    Description: A basic S3 bucket
    Value: !Ref MyS3Bucket
```

Steps:

Simply go to CloudFormation, upload this template as a YAML file, and hit create stack.

### Deactivation of resources
```bash
aws cloudformation delete-stack --stack-name my-stack
```

## Using AWS Step Functions to build an ETL (AWS Glue pipeline)

- Start
- run_job1
- run_crawler1
- check_crawler_status
  - wait
- run_job2
- run_crawler2
- END

- Reusability
  - pipeline by pipeline dev
  - little reusability, generic dev at job level
- Observability
  - built-in and out of the box visibility
  - pipeline and step lvl tracking
- Early rewards to dev effort
- out of box integration with most AWS services

1) AWS Step Functions runs a AWS Glue Start Job with the following parameters
  - job name
  - job parameters
  - sync/async
   - Define the next state in the State Machine Workflow
2) Starting a glue crawler
   - No Out of box crawler task
   - long execution
   - Two Approaches;
     1) Use Step Function task to invoke crawler API; ```waitForTaskToken``` used to get state
     2) Leverage lambda tasks
        - Start Crawler lambda func
        - Get Status lambda crawler (keeps checking till it fetches a ready status)
      - Both of these work in parallel to orchestrate glue job
  
        ```json
        {'crawlername':'crawler1'}
        ```
        ```python
        import json
        import boto3
        def lambda_handler(event,context):
            target = event["crawlername"]
            glueclient = boto3.client('glue')
            glueclient.start_crawler(Name=target)
        ```
      - get runid from crawler as output
        ```json
        {'crawlername':'crawler1'}
        ```
        ```python
        import json
        import boto3
            
        def lambda_handler(event,context):
            target = event['crawlername']
            glueclient = boto3.client('glue')
            response = glueclient.get_crawler(Name=target)
            return {
                'state':response['Crawler']['State']
            }
        ```

Complete Demo Pipeline:

- Amazon RDS (Table)
- job 1 -> S3 (raw)
  - crawler1 -> job2
    - S3 (cleaned)
      - crawler2

### Getting Persistent Files into S3

```python
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: bucket-with-files

  UploadFiles:
    Type: Custom::S3Upload
    Properties:
      ServiceToken: !GetAtt UploadLambda.Arn
      BucketName: !Ref S3Bucket
      Files:
        - Source: https://raw.githubusercontent.com/anshsinghal2002/Cloudformation-POC/main/python_scripts/lambda_function.py
          Destination: lambda_start.py
        - Source: https://raw.githubusercontent.com/anshsinghal2002/Cloudformation-POC/main/python_scripts/lambda_handler.py
          Destination: folder/lambda_status.py

  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: S3Access
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:PutObject
                Resource: !Sub '${S3Bucket.Arn}/*'

  UploadLambda:
    Type: AWS::Lambda::Function
    Properties:
      Handler: index.handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        ZipFile: |
          import boto3
          import cfnresponse
          import urllib.request

          s3 = boto3.client('s3')

          def handler(event, context):
            try:
              bucket = event['ResourceProperties']['BucketName']
              files = event['ResourceProperties']['Files']
              
              for file in files:
                urllib.request.urlretrieve(file['Source'], '/tmp/tempfile')
                s3.upload_file('/tmp/tempfile', bucket, file['Destination'])
              
              cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
            except Exception as e:
              print(e)
              cfnresponse.send(event, context, cfnresponse.FAILED, {})

      Runtime: python3.8
```


