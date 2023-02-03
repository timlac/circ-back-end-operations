import boto3
from glob import glob
import logging
import sys
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv


from metadata.error_file_exception import ErrorFileException
from metadata.file_metadata import Metadata
from helpers import get_filename

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def get_file_paths(path):
    paths = glob(path + '**/*.mp4')
    logging.info("Files found:" + str(len(paths)))
    return paths


class s3Uploader:
    """
    A class that uploads files to AWS S3
    """

    def __init__(self):
        load_dotenv()
        s3_bucket_name = os.environ.get("S3_BUCKET_NAME")
        # Set the name of the bucket and the file you want to upload
        self.bucket_name = s3_bucket_name

        # Create an S3 client
        self.s3 = boto3.client('s3')

    def upload(self, path, file_name):
        """
        Uploads a file to S3
        :param path: the local path
        :param file_name: the file name
        :return:
        """
        self.s3.upload_file(path, self.bucket_name, file_name)

    def file_name_exists(self, file_name):
        """
        :param file_name: check if this filename already exists in bucket
        :return: True if exists, False otherwise
        """
        try:
            # Try to retrieve the metadata for the object with the given key
            self.s3.head_object(Bucket=self.bucket_name, Key=file_name)
        except ClientError as e:
            # If a ClientError is raised, it means that the object does not exist
            # You can go ahead and upload the file
            if e.response['Error']['Code'] == '404':
                return False
            else:
                # If the error code is not 404, it means that there was some other error
                print(f'Error: {e}')
        else:
            # If no exception is raised, it means that the object with the given key exists
            return True


def process_files(directory):
    """
    :param directory: dir to process recursively
    """

    uploader = s3Uploader()

    paths = get_file_paths(directory)

    for filepath in paths:
        try:
            filename = get_filename(filepath)
            metadata = Metadata(filename)

            if not metadata.mix:
                file_name = os.path.basename(filepath)

                if uploader.file_name_exists(file_name):
                    logging.info("file name {} already exists, skipping: ".format(file_name))
                else:
                    logging.info("uploading file: " + str(file_name))
                    # Upload the file to S3
                    uploader.upload(filepath, file_name)

        except ErrorFileException as e:
            logging.info(e)
            continue


path = "/home/tim/work/su-thesis-project/resources/videos/AAC_480p"
process_files(path)
