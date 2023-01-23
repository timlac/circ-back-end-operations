from random import shuffle

import boto3

from back_end.config import s3_bucket_name


def get_bucket_contents():
    s3 = boto3.client("s3")
    bucket_name = s3_bucket_name
    bucket_objects = s3.list_objects(Bucket=bucket_name)["Contents"]
    shuffle(bucket_objects)
    for key in bucket_objects:
        yield key["Key"]
