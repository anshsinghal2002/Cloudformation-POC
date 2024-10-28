import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Amazon S3
AmazonS3_node1730081316654 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ","}, connection_type="s3", format="csv", connection_options={"paths": ["s3://demo-bucket3986y/raw/games.csv"], "recurse": True}, transformation_ctx="AmazonS3_node1730081316654")

# Script generated for node Drop Fields
DropFields_node1730082159755 = DropFields.apply(frame=AmazonS3_node1730081316654, paths=["id", "created_at", "last_move_at", "rated", "white_id", "black_id", "opening_ply"], transformation_ctx="DropFields_node1730082159755")

# Script generated for node Amazon S3
AmazonS3_node1730082393807 = glueContext.write_dynamic_frame.from_options(frame=DropFields_node1730082159755, connection_type="s3", format="csv", connection_options={"path": "s3://demo-bucket3986y/cleaned/", "partitionKeys": []}, transformation_ctx="AmazonS3_node1730082393807")

job.commit()