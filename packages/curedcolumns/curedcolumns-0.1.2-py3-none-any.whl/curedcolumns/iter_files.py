import logging
from pathlib import Path
from typing import Generator

from boto3_type_annotations.s3 import Client

logger = logging.getLogger(__name__)


def iter_files(s3_client: Client, bucket: str, prefix: str = None, file_ext: str = None, **kwargs) -> Generator[
    Path, None, None]:
    """
    This function yields the S3 key (path) of parquet files in an S3 bucket as a generator.

    Args:
        s3_client: AWS S3 service client
        bucket: The name of the S3 bucket to search (str).
        prefix: Folder
        file_ext: Filter by file extension (default: .parquet)

    Yields:
        The S3 key (path) of each parquet file found (str).
    """

    # Default argument values
    file_ext = file_ext or '.parquet'
    prefix = prefix or ''

    # Use a paginator to list objects
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html
    # https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html
    paginator = s3_client.get_paginator("list_objects_v2")

    # Iterate over pages
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix, **kwargs):

        # Loop through S3 objects (files)
        for obj in page.get("Contents", set()):
            s3_key = Path(obj["Key"])
            if s3_key.suffix == file_ext:
                yield s3_key
