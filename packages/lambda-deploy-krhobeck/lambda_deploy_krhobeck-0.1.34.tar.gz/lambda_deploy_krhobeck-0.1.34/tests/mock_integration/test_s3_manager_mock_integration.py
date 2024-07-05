from unittest import TestCase

import boto3
from moto import mock_aws
from mypy_boto3_s3.client import S3Client
from lambda_deploy.s3_manager import check_s3_exists


class TestS3ManagerMockIntegration(TestCase):
    """
    S3 Manager Mock Integration Tests
    """

    def setUp(self):
        self.mock_aws = mock_aws()
        self.mock_aws.start()

        self.aws_session = boto3.Session(region_name="us-east-1")

        self.s3_client: S3Client = self.aws_session.client("s3")
        self.bucket_name = "test-bucket"
        self.s3_client.create_bucket(Bucket=self.bucket_name)

    def tearDown(self):
        self.mock_aws.stop()

    def test_check_s3_exists_success_true(self):
        # Act
        exists = check_s3_exists(self.aws_session, self.bucket_name)

        # Assert
        self.assertTrue(
            exists,
            "The bucket should exist but check_s3_exists returned False.",
        )

    def test_check_s3_exists_success_false(self):
        # Arrange
        non_existent_bucket = "nonexistent-bucket"

        # Act
        exists = check_s3_exists(self.aws_session, non_existent_bucket)

        # Assert
        self.assertFalse(
            exists,
            "The bucket does not exist but check_s3_exists returned True.",
        )
