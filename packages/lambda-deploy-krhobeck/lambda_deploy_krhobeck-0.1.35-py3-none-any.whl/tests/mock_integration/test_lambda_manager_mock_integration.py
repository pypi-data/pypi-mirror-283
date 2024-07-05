import os
from unittest import TestCase
from unittest.mock import patch

import boto3
from moto import mock_aws

from lambda_deploy.lambda_manager import (
    setup_lambdas,
    create_or_update_lambda_role,
    create_iam_policy_document,
)


class TestLambdaManagerMockIntegration(TestCase):
    """
    Test Lambda Manager Mock Integration
    """

    def setUp(self):
        self.mock_aws = mock_aws()
        self.mock_aws.start()
        self.aws_session = boto3.Session(region_name="us-east-1")
        self.s3_client = self.aws_session.client("s3")
        self.bucket_name = "test-bucket"
        self.s3_client.create_bucket(Bucket=self.bucket_name)
        self.file_path = "/tmp/test_lambda_code.zip"
        self.s3_key = "test_lambda_code.zip"

        # Create a test file
        with open(self.file_path, "wb") as f:
            f.write(os.urandom(1024))  # Write random bytes to file

        # Upload the file to S3
        with open(self.file_path, "rb") as f:
            self.s3_client.upload_fileobj(
                Fileobj=f, Bucket=self.bucket_name, Key=self.s3_key
            )

    def tearDown(self):
        self.mock_aws.stop()
        os.remove(self.file_path)

    def test_create_iam_policy_document(self):
        permissions = [
            {
                "resource_type": "S3",
                "resource_name": "my-bucket",
                "actions": ["s3:GetObject", "s3:ListBucket"],
            },
            {
                "resource_type": "DynamoDB",
                "resource_name": "MyTable",
                "actions": ["dynamodb:Query", "dynamodb:Scan"],
            },
            {
                "resource_type": "Cognito",
                "resource_name": "us-east-1_XXXXX",
                "actions": ["cognito-idp:AdminCreateUser"],
            },
        ]
        policy_document = create_iam_policy_document(
            self.aws_session, permissions
        )
        # Check the structure of the policy document
        self.assertIn("Statement", policy_document)
        self.assertEqual(len(policy_document["Statement"]), len(permissions))
        self.assertIn(
            "s3:GetObject", policy_document["Statement"][0]["Action"]
        )
        self.assertIn(
            "cognito-idp:AdminCreateUser",
            policy_document["Statement"][2]["Action"],
        )

    def test_create_or_update_lambda_role(self):
        iam_config = {
            "permissions": [
                {
                    "resource_type": "S3",
                    "resource_name": "my-bucket",
                    "actions": ["s3:GetObject", "s3:ListBucket"],
                }
            ]
        }
        role_name = "test-lambda-role"
        role_arn = create_or_update_lambda_role(
            self.aws_session, role_name, iam_config
        )
        # Verify the role is created or updated
        self.assertTrue(role_arn.startswith("arn:aws:iam::"))

    def test_setup_lambdas(self):
        lambda_functions = [
            {
                "name": "test-function",
                "runtime": "python3.8",
                "role_name": "test-lambda-role",
                "handler": "lambda_function.handler",
                "file_path": self.file_path,
                "s3_bucket": self.bucket_name,
                "s3_key": self.s3_key,
                "description": "Test function",
                "timeout": 120,
                "memory_size": 256,
                "iam_config": {
                    "permissions": [
                        {
                            "resource_type": "S3",
                            "resource_name": "my-bucket",
                            "actions": ["s3:GetObject", "s3:ListBucket"],
                        }
                    ]
                },
            }
        ]
        # Patching to simulate the decorated list
        with patch(
            "lambda_deploy.lambda_manager.lambda_functions", lambda_functions
        ):
            setup_lambdas(self.aws_session)
