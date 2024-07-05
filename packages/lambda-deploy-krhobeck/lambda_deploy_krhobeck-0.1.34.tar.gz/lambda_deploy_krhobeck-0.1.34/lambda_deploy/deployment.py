import os

import boto3
import logging
from boto3 import Session
from lambda_deploy.lambda_manager import setup_lambdas
from lambda_deploy.api_gateway_manager import setup_api_gateway
from lambda_deploy.layer_manager import setup_layers
from mypy_boto3_s3.client import S3Client


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_session() -> Session:
    return boto3.Session()


def check_connection(session: Session) -> None:
    s3: S3Client = session.client("s3")
    try:
        s3.list_buckets()
    except Exception as e:
        print(f"Failed to connect to AWS: {str(e)}")
        raise


def read_existing_hash(
    source_path: str, hash_filename: str = "layer_hash.txt"
) -> str:
    """Read the existing hash from a file, or return an empty string if the
    file does not exist."""
    hash_file_path = os.path.join(source_path, hash_filename)
    try:
        with open(hash_file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""


def deploy(
    source_path: str,
    layer_name: str,
    user_pool_id: str,
    domain_name: str,
    certificate_arn: str,
    layer_directories=None,
    external_packages=None,
) -> None:
    """
    Deploys all lambda functions and layers, sets up API Gateway,
    and configures IAM roles and permissions.
    :return:
    """
    logging.info("Starting deployment process.")
    logging.info("Creating a new boto3 session.")
    boto3_session: Session = get_session()
    logging.info("Checking connection to AWS services.")
    check_connection(boto3_session)
    existing_hash = read_existing_hash(source_path)
    layer_arn = None
    if layer_directories or external_packages:
        logging.info(
            "Setting up Lambda layers with provided directories and packages."
        )
        layer_arn = setup_layers(
            source_path,
            layer_name,
            layer_directories,
            external_packages,
            boto3_session,
            existing_hash,
        )
    logging.info("Aggregating lambda function configurations.")
    logging.info("Setting up lambda functions.")
    setup_lambdas(boto3_session, layer_arn)
    logging.info("Setting up API Gateway.")
    setup_api_gateway(
        boto3_session, user_pool_id, domain_name, certificate_arn
    )
    logging.info("Deployment process completed successfully.")
