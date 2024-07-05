import pathlib

import pytest
from boto3_type_annotations.s3 import Client
import moto

import curedcolumns


@moto.mock_aws
def test_iter_files(s3_client: Client, bucket: str):
    key: pathlib.Path
    for key in curedcolumns.iter_files(s3_client=s3_client, bucket=bucket):
        assert isinstance(key, pathlib.Path), 'Invalid data type'
        assert key.suffix == '.parquet', 'Invalid file extension'
