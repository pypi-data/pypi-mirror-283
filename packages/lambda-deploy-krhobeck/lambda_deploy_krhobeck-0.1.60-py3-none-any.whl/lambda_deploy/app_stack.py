from aws_cdk import (  # Duration,
    Stack,
    Duration,  # aws_sqs as sqs,
)
from aws_cdk import aws_ecr as ecr
from constructs import Construct
from aws_cdk import aws_lambda as lambda_


class LambdaDeployStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create ECR repository
        repository = ecr.Repository(self, "LambdaRepository")

        # Assuming the repository is already created and the image is pushed
        repository = ecr.Repository.from_repository_name(
            self, "ExistingRepo", repository_name="YourRepositoryName"
        )

        # Define the Lambda function with the Docker image
        lambda_function = lambda_.DockerImageFunction(
            self,
            "MyDockerLambda",
            code=lambda_.DockerImageCode.from_ecr(repository),
            memory_size=1024,
            # example configuration
            timeout=Duration.seconds(300),
        )
