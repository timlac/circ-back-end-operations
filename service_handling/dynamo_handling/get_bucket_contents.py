from random import shuffle

import boto3
import os
from dotenv import load_dotenv

from helpers import get_filename
from metadata.file_metadata import Metadata

import boto3

s3 = boto3.client("s3")


def list_all_objects_in_bucket():
    load_dotenv()
    s3_bucket_name = os.environ.get("S3_BUCKET_NAME")

    continuation_token = None
    objects = []

    while True:
        if continuation_token:
            kwargs = {'ContinuationToken': continuation_token}
        else:
            kwargs = {}

        response = s3.list_objects_v2(Bucket=s3_bucket_name, **kwargs)
        objects += response.get("Contents", [])
        continuation_token = response.get("NextContinuationToken")

        if not continuation_token:
            break

    shuffle(objects)

    return objects


def get_bucket_contents():
    load_dotenv()
    s3_bucket_name = os.environ.get("S3_BUCKET_NAME")
    s3 = boto3.client("s3")
    bucket_name = s3_bucket_name
    bucket_objects = s3.list_objects(Bucket=bucket_name)["Contents"]

    print(len(bucket_objects))

    shuffle(bucket_objects)
    for key in bucket_objects:
        yield key["Key"]


def main():
    ret = list_all_objects_in_bucket()
    print(len(ret))



if __name__ == "__main__":
    main()
