import base64
from typing import List

import boto3
import docker


def generate_dockerfiles(
    lambda_functions: List,
    source_path,
    base_image,
    requirements_path=None,
    copy_paths=None,
):
    for func in lambda_functions:
        handler_path = "handlers." + func._lambda_meta.get("handler")
        dockerfile_name = f"Dockerfile_{func._lambda_meta.get('name')}"

        dockerfile_content = [
            f"FROM {base_image}",
            "WORKDIR /var/task",
            "ENV PYTHONPATH=/var/task",
        ]

        if requirements_path:
            dockerfile_content.append(f"COPY {requirements_path} ./")
            dockerfile_content.append("RUN pip install -r requirements.txt")

        if copy_paths:
            for path in copy_paths:
                dockerfile_content.append(f"COPY {path} ./")
        dockerfile_content.append(f'CMD ["{handler_path}"]')

        dockerfile_path = f"{source_path}/dockerfiles/{dockerfile_name}"
        with open(dockerfile_path, "w") as file:
            file.write("\n".join(dockerfile_content))

        print(
            f"Dockerfile for {func._lambda_meta.get('name')} created at: {dockerfile_path}"
        )


def build_and_push_images(
    lambda_functions: List, source_path, repository_name_base, tag="latest"
):
    client = docker.from_env()
    ecr_client = boto3.client("ecr")
    account_id = boto3.client("sts").get_caller_identity().get("Account")
    region = boto3.session.Session().region_name

    image_uris = []

    # Loop over each function to build and push its Docker image
    for func in lambda_functions:
        # Create a unique repository name for each function
        repository_name = (
            f"{repository_name_base}_{func._lambda_meta.get('name')}"
        )
        image_tag = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{tag}"

        # Ensure repository exists
        try:
            ecr_client.create_repository(repositoryName=repository_name)
        except ecr_client.exceptions.RepositoryAlreadyExistsException:
            pass

        # Authenticate to ECR
        token = ecr_client.get_authorization_token()
        username, password = (
            base64.b64decode(
                token["authorizationData"][0]["authorizationToken"]
            )
            .decode()
            .split(":")
        )
        registry = token["authorizationData"][0]["proxyEndpoint"]
        client.login(username, password, registry=registry)

        # Build the Docker image
        dockerfile_path = (
            f"./dockerfiles/Dockerfile_{func._lambda_meta.get('name')}"
        )
        image, _ = client.images.build(
            path=source_path,
            dockerfile=dockerfile_path,
            tag=image_tag,
            rm=True,
        )
        client.images.push(image_tag)

        image_uris.append(image_tag)

    return image_uris
