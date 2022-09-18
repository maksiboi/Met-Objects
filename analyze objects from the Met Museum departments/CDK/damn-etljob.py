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
    connection_options={"paths": ["s3://damnbuckettask"], "recurse": True},
    transformation_ctx="S3bucket_node1",
)

# Script generated for node ApplyMapping
ApplyMapping_node2 = ApplyMapping.apply(
    frame=S3bucket_node1,
    mappings=[
        ("objectID", "int", "objectID", "int"),
        ("isHighlight", "boolean", "isHighlight", "boolean"),
        ("accessionNumber", "string", "accessionNumber", "string"),
        ("accessionYear", "string", "accessionYear", "string"),
        ("isPublicDomain", "boolean", "isPublicDomain", "boolean"),
        ("primaryImage", "string", "primaryImage", "string"),
        ("department", "string", "department", "string"),
        ("objectName", "string", "objectName", "string"),
        ("title", "string", "title", "string"),
        ("culture", "string", "culture", "string"),
        ("period", "string", "period", "string"),
        ("dynasty", "string", "dynasty", "string"),
        ("reign", "string", "reign", "string"),
        ("objectDate", "string", "objectDate", "string"),
        ("objectBeginDate", "int", "objectBeginDate", "int"),
        ("objectEndDate", "int", "objectEndDate", "int"),
        ("medium", "string", "medium", "string"),
        ("dimensions", "string", "dimensions", "string"),
        ("geographyType", "string", "geographyType", "string"),
        ("city", "string", "city", "string"),
        ("state", "string", "state", "string"),
        ("country", "string", "country", "string"),
        ("region", "string", "region", "string"),
        ("classification", "string", "classification", "string"),
        ("metadataDate", "string", "metadataDate", "string"),
        ("repository", "string", "repository", "string"),
        ("isTimelineWork", "boolean", "isTimelineWork", "boolean"),
        ("GalleryNumber", "string", "GalleryNumber", "string"),
        ("constituentID", "int", "constituentID", "int"),
        ("constituent_role", "string", "constituent_role", "string"),
        ("constituent_name", "string", "constituent_name", "string"),
        (
            "constituent_constituentULAN_URL",
            "string",
            "constituent_constituentULAN_URL",
            "string",
        ),
        ("Depth", "double", "Depth", "string"),
        ("Height", "double", "Height", "string"),
        ("Width", "double", "Width", "string"),
        ("Lenght", "double", "Lenght", "string"),
        ("measurment_elementName", "string", "measurment_elementName", "string"),
        (
            "measurment_elementDescription",
            "string",
            "measurment_elementDescription",
            "string",
        ),
    ],
    transformation_ctx="ApplyMapping_node2",
)

# Script generated for node S3 bucket
S3bucket_node3 = glueContext.write_dynamic_frame.from_options(
    frame=ApplyMapping_node2,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://damntargetbucket",
        "partitionKeys": ["department"],
    },
    format_options={"compression": "uncompressed"},
    transformation_ctx="S3bucket_node3",
)

job.commit()