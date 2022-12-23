import boto3
from datetime import date
from . import dyconfig
from . import setup
from . import reserve_repository
from . import csv_factory

logger = setup.get_logger(__name__)
origin_csv_dir = dyconfig.get("output_csv", "output_path")
target_bucket = dyconfig.get("upload_csv", "target_s3_bucket")
TARGET_PATH = "feed/transaction"


def upload(filename_list: list[str]) -> None:
    s3_client = boto3.client('s3')

    for filename in filename_list:
        origin_filename = f"{origin_csv_dir}/{filename}"
        uploaded_filename = f"{TARGET_PATH}/{filename}"
        s3_client.upload_file(origin_filename, target_bucket, uploaded_filename)
