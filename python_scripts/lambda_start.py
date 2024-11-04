import json
import boto3

def lambda_handler(event, context):
    try:
        target = event["crawlername"]
        glueclient = boto3.client('glue')
        glueclient.start_crawler(Name=target)
        return {
            'statusCode': 200,
            'body': json.dumps('Crawler started successfully')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }