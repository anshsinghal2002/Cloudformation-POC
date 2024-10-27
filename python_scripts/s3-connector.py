import boto3

# Create an S3 client
s3 = boto3.client('s3',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='YOUR_BUCKET_REGION'
)

# Specify your bucket name
bucket_name = 'your-bucket-name'

# List objects in the bucket
response = s3.list_objects_v2(Bucket=bucket_name)

# Print object keys (file names)
for obj in response['Contents']:
    print(obj['Key'])

# Download a specific file
file_key = 'path/to/your/file.txt'
s3.download_file(bucket_name, file_key, 'local_file.txt')