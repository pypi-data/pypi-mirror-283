import json
from unittest import TestCase
from unittest.mock import patch

import boto3
from moto import mock_aws

from lambda_deploy.api_gateway_manager import (
    create_rest_api,
    deploy_api,
    create_resource,
    setup_method,
    setup_api_gateway,
)


class MockApiGatewayManagerMockIntegrationTest(TestCase):
    """
    Mock Integration Test For Api Gateway
    """

    def setUp(self):
        self.mock_aws = mock_aws()
        self.mock_aws.start()
        self.aws_session = boto3.Session(region_name="us-east-1")
        self.api_gateway_client = self.aws_session.client("apigateway")
        self.s3_client = self.aws_session.client("s3")
        self.bucket_name = "test-bucket"
        self.s3_client.create_bucket(Bucket=self.bucket_name)

        self.cognito_client = self.aws_session.client("cognito-idp")
        self.acm_client = self.aws_session.client("acm")

        # Create a fake user pool
        user_pool_response = self.cognito_client.create_user_pool(
            PoolName="TestPool"
        )
        self.user_pool_id = user_pool_response["UserPool"]["Id"]

        # Create a fake certificate
        cert_response = self.acm_client.request_certificate(
            DomainName="example.com"
        )
        self.certificate_arn = cert_response["CertificateArn"]

    def tearDown(self):
        self.mock_aws.stop()

    def test_create_rest_api(self):
        """Test creating a new REST API."""
        api_name = "TestAPI"
        api_id = create_rest_api(self.api_gateway_client, api_name)
        self.assertIsNotNone(api_id)

    def test_create_resource(self):
        """Test creating a resource within the REST API."""
        api_id = create_rest_api(self.api_gateway_client, "TestAPI")
        root_id = self.api_gateway_client.get_resources(restApiId=api_id)[
            "items"
        ][0]["id"]
        path_part = "test"
        resource_id = create_resource(
            self.api_gateway_client, api_id, root_id, path_part
        )
        self.assertIsNotNone(resource_id)

    def test_setup_method(self):
        """Test setting up a method for a resource."""
        domain_name = "api.example.com"
        api_id = create_rest_api(self.api_gateway_client, "TestAPI")
        root_id = self.api_gateway_client.get_resources(restApiId=api_id)[
            "items"
        ][0]["id"]
        resource_id = create_resource(
            self.api_gateway_client, api_id, root_id, "test"
        )
        lambda_function_data = {
            "http_method": "GET",
            "lambda_arn": "arn:aws:lambda:us-east-1:123456789012:function:"
            "my-function",
            "user_pool_id": self.user_pool_id,
            "domain_name": domain_name,
            "certificate_arn": self.certificate_arn,
        }
        setup_method(
            self.api_gateway_client, api_id, resource_id, lambda_function_data
        )

    def test_deploy_api(self):
        """Test deploying the API with resources and methods."""
        domain_name = "api.example.com"
        api_id = create_rest_api(self.api_gateway_client, "TestAPI")

        # Create a resource at the root level
        root_id = self.api_gateway_client.get_resources(restApiId=api_id)[
            "items"
        ][0]["id"]
        resource_id = create_resource(
            self.api_gateway_client, api_id, root_id, "resource1"
        )

        # Setup a dummy method for this resource
        lambda_function_data = {
            "http_method": "GET",
            "lambda_arn": "arn:aws:lambda:us-east-1:123456789012:function"
            ":exampleFunction",
            "user_pool_id": self.user_pool_id,
            "domain_name": domain_name,
            "certificate_arn": self.certificate_arn,
            "cors_config": None,
        }
        setup_method(
            self.api_gateway_client, api_id, resource_id, lambda_function_data
        )

        # Deploy the API after setting up the method
        deploy_api(self.api_gateway_client, api_id, "Dev")

        # Print all resources to verify
        all_resources = self.api_gateway_client.get_resources(restApiId=api_id)
        print("Deployed API Resources:", json.dumps(all_resources, indent=4))

    def test_setup_api_gateway(self):
        """Test the complete setup of API Gateway with custom domain and user pool."""
        domain_name = "api.example.com"
        with patch(
            "lambda_deploy.api_gateway_manager.lambda_functions",
            new_callable=lambda: [
                {
                    "name": "TestFunction",
                    "endpoint": "test",
                    "http_method": "GET",
                    "lambda_arn": "arn:aws:lambda:us-east-1:123456789012:function:my-function",
                    "user_pool_id": self.user_pool_id,
                    "domain_name": domain_name,
                    "certificate_arn": self.certificate_arn,
                }
            ],
        ):
            setup_api_gateway(
                self.aws_session,
                user_pool_id=self.user_pool_id,
                certificate_arn=self.certificate_arn,
                domain_name=domain_name,
            )
            # Additional code to check setup_api_gateway behavior can be added here.

        # Print the setup details for debugging
        print("User Pool ID:", self.user_pool_id)
        print("Certificate ARN:", self.certificate_arn)
        print("Domain Name:", domain_name)
