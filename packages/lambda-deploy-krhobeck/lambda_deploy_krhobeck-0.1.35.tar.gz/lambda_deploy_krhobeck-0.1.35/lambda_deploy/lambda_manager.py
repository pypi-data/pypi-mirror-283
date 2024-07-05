import json
import os
import zipfile
from typing import List

from boto3 import Session
from mypy_boto3_iam.client import IAMClient
from mypy_boto3_s3.client import S3Client
from lambda_deploy.decorators import lambda_functions
from lambda_deploy.pydantic_models import IAMConfig, ResourcePermission


def get_account_id(session):
    """Retrieve the account ID using an AWS STS client."""
    sts_client = session.client("sts")
    identity = sts_client.get_caller_identity()
    return identity["Account"]


def upload_lambda_code(
    session: Session, lambda_function_data: object, source_path: str
):
    """Uploads lambda function code to an S3 bucket."""
    s3: S3Client = session.client("s3")
    function_path = (
        source_path + lambda_function_data._lambda_meta["file_path"]
    )
    print("function path is", function_path)

    # Determine the zip file path
    zip_path = function_path + ".zip"

    # Create a zip file
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(function_path, arcname=os.path.basename(function_path))

    # Upload the zip file
    print("Zip file path is", zip_path)
    with open(zip_path, "rb") as zip_file:
        s3.upload_fileobj(
            Fileobj=zip_file,
            Bucket=lambda_function_data._lambda_meta["s3_bucket"],
            Key=lambda_function_data._lambda_meta["s3_key"],
        )
    os.remove(zip_path)


def create_iam_policy_document(session, permissions: List[ResourcePermission]):
    """Generate an IAM policy document from permissions."""
    account_id = get_account_id(session)
    region = session.region_name
    statements = []

    for perm in permissions:
        resource_type = perm.resource_type.lower()
        actions = perm.actions
        if resource_type == "s3":
            resource = [
                f"arn:aws:s3:::{perm.resource_name}",
                f"arn:aws:s3:::{perm.resource_name}/*",
            ]
        elif resource_type == "dynamodb":
            resource = [
                f"arn:aws:dynamodb:{region}:{account_id}:table/"
                f"{perm.resource_name}"
            ]
        elif resource_type == "cognito":
            resource = [
                f"arn:aws:cognito-idp:{region}:{account_id}:userpool/"
                f"{perm.resource_name}"
            ]
        else:
            resource = [
                f"arn:aws:{resource_type}:{region}:{account_id}:"
                f"{perm.resource_name}"
            ]

        statements.append(
            {"Effect": "Allow", "Action": actions, "Resource": resource}
        )

    return {"Version": "2012-10-17", "Statement": statements}


def create_or_update_lambda_role(
    session: Session, role_name: str, iam_config: IAMConfig
):
    iam: IAMClient = session.client("iam")
    policy_document = create_iam_policy_document(
        session, iam_config.permissions
    )
    policy_name = f"{role_name}-policy"

    # Check if the policy already exists
    try:
        existing_policy = iam.get_policy(
            PolicyArn=f"arn:aws:iam::{get_account_id(session)}:policy/{policy_name}"
        )
    except iam.exceptions.NoSuchEntityException:
        existing_policy = None

    if not existing_policy:
        policy = iam.create_policy(
            PolicyName=policy_name, PolicyDocument=json.dumps(policy_document)
        )
        policy_arn = policy["Policy"]["Arn"]
    else:
        policy_arn = existing_policy["Policy"]["Arn"]

    # Create or update the role
    try:
        role = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "lambda.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                }
            ),
            Description="Lambda execution role",
        )
        role_arn = role["Role"]["Arn"]
    except iam.exceptions.EntityAlreadyExistsException:
        role_arn = iam.get_role(RoleName=role_name)["Role"]["Arn"]
    iam.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
    return role_arn


def get_lambda_function(lambda_client, function_name):
    try:
        return lambda_client.get_function(FunctionName=function_name)
    except lambda_client.exceptions.ResourceNotFoundException:
        return None


def publish_new_version(lambda_client, function_name):
    response = lambda_client.publish_version(FunctionName=function_name)
    return response["Version"]


def update_function_code(lambda_client, function_name, s3_bucket, s3_key):
    lambda_client.update_function_code(
        FunctionName=function_name,
        S3Bucket=s3_bucket,
        S3Key=s3_key,
        Publish=True,
    )


def setup_lambda_function(session, lambda_function_data, layer_arn):
    lambda_client = session.client("lambda")
    function_exists = get_lambda_function(
        lambda_client, lambda_function_data._lambda_meta["name"]
    )

    if function_exists:
        # Update existing function code
        update_function_code(
            lambda_client,
            lambda_function_data._lambda_meta["name"],
            lambda_function_data._lambda_meta["s3_bucket"],
            lambda_function_data._lambda_meta["s3_key"],
        )
    else:
        # Create new Lambda function
        lambda_client.create_function(
            FunctionName=lambda_function_data._lambda_meta["name"],
            Runtime=lambda_function_data._lambda_meta["runtime"],
            Role=lambda_function_data._lambda_meta["role_arn"],
            Handler=lambda_function_data._lambda_meta["handler"],
            Code={
                "S3Bucket": lambda_function_data._lambda_meta["s3_bucket"],
                "S3Key": lambda_function_data._lambda_meta["s3_key"],
            },
            Description=lambda_function_data._lambda_meta.get(
                "description", "Deployed via automated system"
            ),
            Timeout=lambda_function_data._lambda_meta.get("timeout", 500),
            MemorySize=lambda_function_data._lambda_meta.get(
                "memory_size", 128
            ),
            Layers=[layer_arn],
            Publish=True,
        )


def setup_lambdas(session, layer_arn=None):
    for lambda_function_data in lambda_functions:
        setup_lambda_function(session, lambda_function_data, layer_arn)
