import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 bucket
S3bucket_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://damn-final-raw-bucket/Twitter/"],
        "recurse": True,
    },
    transformation_ctx="S3bucket_node1",
)

# Script generated for node ApplyMapping
ApplyMapping_node2 = ApplyMapping.apply(
    frame=S3bucket_node1,
    mappings=[
        ("coin_name", "string", "coin_name", "string"),
        ("created_at", "string", "created_at", "string"),
        ("id", "bigint", "id", "string"),
        ("text", "string", "text", "string"),
        ("hashtags", "string", "hashtags", "string"),
        ("retweet_count", "int", "retweet_count", "int"),
        ("user_id", "bigint", "user_id", "string"),
        ("user_followers_count", "int", "user_followers_count", "int"),
        ("user_friends_count", "int", "user_friends_count", "int"),
    ],
    transformation_ctx="ApplyMapping_node2",
)

# Script generated for node S3 bucket
S3bucket_node3 = glueContext.write_dynamic_frame.from_options(
    frame=ApplyMapping_node2,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://damn-final-parquet-bucket/Twitter/",
        "partitionKeys": ["coin_name"],
    },
    format_options={"compression": "uncompressed"},
    transformation_ctx="S3bucket_node3",
)

job.commit()
