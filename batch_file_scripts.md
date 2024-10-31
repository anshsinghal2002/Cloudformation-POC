## Outline

- clone github for relevant files
- create s3 bucket and create relevant folders
- copy into s3 relevant script and data files `init-bucket-uniqus`
- launch cloudformation with final yaml file which
  - creates an input s3 bucket
    - executes a lambda function to upload files from `init-bucket-uniqus` to `data-in-bucket`
    - create relevant subfolders in `data-in-bucket`
  - create required lambda functions and glue jobs based on scripts provided in `data-in-bucket`
  - once lambda functions and glue jobs are in place, create etl pipeline using Step Functions and store output in `data-out-bucket`. Create endpoint to invoke step function execution and also display cleaned output in an external database

Then we also need an executable batch file to delete the created buckets and deallocate the resources spun up by the cfn. 
## Batch File Scripts

### Deleting S3 Buckets

```bash
for i in $(aws s3 ls | cut -d" " -f3); do
  aws s3 rb s3://$i --force
done
```

or using python script executed by a lambda function
### Rolling back cfn template

```bash
aws cloudformation rollback-stack --stack-name <your-stack-name>
```

### Executing cfn yaml

```bash
aws cloudformation deploy \
  --template-file final_stack_files/testpipeline.yaml \
  --stack-name test-pipeline \
  --capabilities CAPABILITY_IAM
```

