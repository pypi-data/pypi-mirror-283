import subprocess

import boto3
import logging

from aws_cdk import App
from boto3 import Session

from lambda_deploy.docker_manager import (
    build_and_push_images,
    generate_dockerfiles,
)
from lambda_deploy.app_stack import LambdaDeployStack
from lambda_deploy.lambda_manager import setup_lambdas
from lambda_deploy.api_gateway_stack import setup_api_gateway
from mypy_boto3_s3.client import S3Client
from lambda_deploy.decorators import lambda_functions


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


def deploy(
    source_path: str,
    user_pool_id: str,
    domain_name: str,
    certificate_arn: str,
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
    # check_connection(boto3_session)
    # generate_dockerfiles(
    #     lambda_functions=lambda_functions,
    #     source_path=source_path,
    #     base_image="public.ecr.aws/lambda/python:3.10",
    #     requirements_path="./requirements.txt",
    #     copy_paths=["./src"],
    # )
    #
    # repository_name = "lambda_deploy_docker"
    # image_uris = build_and_push_images(
    #     lambda_functions, source_path, repository_name
    # )
    #
    # # Proceed with setting up API Gateway, Lambda functions, etc.
    # print(f"Docker Image URI: {image_uris}")
    # logging.info("Setting up lambda functions.")
    # setup_lambdas(boto3_session, image_uris)
    # logging.info("Setting up API Gateway.")
    # setup_api_gateway(
    #     boto3_session, user_pool_id, domain_name, certificate_arn
    # )
    app = App()
    LambdaDeployStack(app, "LambdaDeployStack")
    app.synth()
    subprocess.run(
        ["cdk", "deploy", "--require-approval", "never"], check=True
    )
    logging.info("Deployment process completed successfully.")
