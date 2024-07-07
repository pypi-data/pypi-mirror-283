from aws_cdk import aws_lambda as _lambda, core


class LambdaDeployStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Define the path to your local Dockerfile for the base image
        docker_asset = DockerImageAsset(
            self,
            "LambdaBaseImage",
            directory="path/to/dockerfile_directory",
            file="Dockerfile_base",
        )

        # Function 1
        lambda_1 = _lambda.DockerImageFunction(
            self,
            "LambdaFunctionOne",
            code=_lambda.DockerImageCode.from_ecr(
                repository=docker_asset.repository,
                tag=docker_asset.image_uri.split(":")[
                    -1
                ],  # Use the latest tag from asset
            ),
            environment={
                "AWS_LAMBDA_EXEC_WRAPPER": "/opt/extensions/my-extension"
            },
            handler="index.handler_one",
        )

        # Function 2
        lambda_2 = _lambda.DockerImageFunction(
            self,
            "LambdaFunctionTwo",
            code=_lambda.DockerImageCode.from_ecr(
                repository=docker_asset.repository,
                tag=docker_asset.image_uri.split(":")[
                    -1
                ],  # Use the latest tag from asset
            ),
            environment={
                "AWS_LAMBDA_EXEC_WRAPPER": "/opt/extensions/my-extension"
            },
            handler="index.handler_two",
        )
