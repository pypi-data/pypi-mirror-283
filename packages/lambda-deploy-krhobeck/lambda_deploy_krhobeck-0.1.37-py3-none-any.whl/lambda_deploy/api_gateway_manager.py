import boto3
from boto3 import Session
from mypy_boto3_apigateway.client import APIGatewayClient
from lambda_deploy.decorators import (
    lambda_functions,
)
from lambda_deploy.lambda_manager import get_account_id


def create_rest_api(api_gateway: APIGatewayClient, api_name: str):
    """Create a new REST API and return its details."""
    response = api_gateway.create_rest_api(name=api_name)
    return response["id"]


def get_root_resource_id(api_gateway: APIGatewayClient, api_id: str):
    """Retrieve the root resource ID for the given API."""
    response = api_gateway.get_resources(restApiId=api_id)
    for item in response["items"]:
        if item["path"] == "/":
            return item["id"]
    return None


def create_cognito_authorizer(api_gateway, api_id, user_pool_id):
    """
    Create a Cognito user pool authorizer for the API Gateway.
    """
    account_id = get_account_id(boto3.Session("us-east-2"))
    response = api_gateway.create_authorizer(
        restApiId=api_id,
        name="CognitoAuthorizer",
        type="COGNITO_USER_POOLS",
        providerARNs=[
            f"arn:aws:cognito-idp:{boto3.Session().region_name}:"
            f"{account_id}:userpool/{user_pool_id}"
        ],
        identitySource="method.request.header.Authorization",
        authType="cognito_user_pools",
    )
    return response["id"]


def create_resource(
    api_gateway: APIGatewayClient, api_id: str, parent_id: str, path_part: str
):
    """Create a resource within the REST API."""
    response = api_gateway.create_resource(
        restApiId=api_id, parentId=parent_id, pathPart=path_part
    )
    return response["id"]


def create_custom_domain(api_gateway, domain_name, certificate_arn):
    """
    Create a custom domain name for the API Gateway.
    """
    response = api_gateway.create_domain_name(
        domainName=domain_name, certificateArn=certificate_arn
    )
    return response["distributionDomainName"]


def link_custom_domain(api_gateway, domain_name, api_id, stage_name):
    """
    Create a base path mapping that links the custom domain to an API deployment.
    """
    api_gateway.create_base_path_mapping(
        domainName=domain_name,
        restApiId=api_id,
        stage=stage_name,
        basePath="(empty for root)",  # or specify a base path
    )


def setup_method(
    api_gateway: APIGatewayClient,
    api_id: str,
    resource_id: str,
    lambda_function_data,
):
    """Setup a method for a resource, with optional CORS and authorizer."""
    http_method = lambda_function_data["http_method"]
    cors_config = lambda_function_data.get("cors_config")

    try:
        api_gateway.get_method(
            restApiId=api_id, resourceId=resource_id, httpMethod=http_method
        )
    except api_gateway.exceptions.ClientError:
        api_gateway.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=http_method,
            authorizationType="COGNITO_USER_POOLS",
        )

    uri = (
        f"arn:aws:apigateway:{boto3.Session().region_name}:lambda:path/"
        f"2015-03-31/functions/{lambda_function_data['lambda_arn']}/invocations"
    )
    api_gateway.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod=http_method,
        type="AWS_PROXY",
        integrationHttpMethod="POST",
        uri=uri,
    )

    # Setup CORS if configured
    if cors_config:
        allow_origin = "method.response.header.Access-Control-Allow-Origin"
        allow_headers = "method.response.header.Access-Control-Allow-Headers"
        allow_methods = "method.response.header.Access-Control-Allow-Methods"
        api_gateway.put_method_response(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=http_method,
            statusCode="200",
            responseParameters={
                allow_origin: True,
                allow_headers: True,
                allow_methods: True,
            },
        )
        integration_resp_parameters = {
            allow_origin: f"'{cors_config.allowed_origin}'",
            allow_headers: f"'{cors_config.allowed_headers}'",
            allow_methods: f"'{cors_config.allowed_methods}'",
        }
        api_gateway.put_integration_response(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod=http_method,
            statusCode="200",
            responseParameters=integration_resp_parameters,
        )


def deploy_api(api_gateway: APIGatewayClient, api_id: str, stage_name: str):
    """Deploy the API to make it available to clients."""
    api_gateway.create_deployment(restApiId=api_id, stageName=stage_name)


def setup_api_gateway(
    session: Session, user_pool_id, domain_name, certificate_arn
):
    api_gateway = session.client("apigateway")
    for func_data in lambda_functions:
        api_name = f"{func_data['name']} API"
        api_id = create_rest_api(api_gateway, api_name)
        root_id = get_root_resource_id(api_gateway, api_id)
        resource_id = create_resource(
            api_gateway, api_id, root_id, func_data["endpoint"]
        )

        create_cognito_authorizer(api_gateway, api_id, user_pool_id)
        setup_method(api_gateway, api_id, resource_id, func_data)
        deploy_api(api_gateway, api_id, "Dev")

        # Setup custom domain and link it
        custom_domain = create_custom_domain(
            api_gateway, domain_name, certificate_arn
        )
        link_custom_domain(api_gateway, domain_name, api_id, "Dev")
        print(f"API available at: https://{custom_domain}")
