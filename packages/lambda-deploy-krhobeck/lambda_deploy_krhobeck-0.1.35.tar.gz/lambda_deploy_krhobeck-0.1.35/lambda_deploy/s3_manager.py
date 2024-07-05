from boto3 import Session
from botocore.exceptions import ClientError
from mypy_boto3_s3 import S3Client


def check_s3_exists(session: Session, bucket_name: str) -> bool:
    s3_client: S3Client = session.client("s3")
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        error_code = int(e.response["Error"]["Code"])
        if error_code == 404:
            return False
        raise
