import base64
import os
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
    dockerfiles_path = os.path.join(source_path, "dockerfiles")
    os.makedirs(dockerfiles_path, exist_ok=True)

    # Create a base Dockerfile
    base_dockerfile_name = "Dockerfile_base"
    base_dockerfile_content = [
        f"FROM {base_image}",
        "WORKDIR /var/task",
        "ENV PYTHONPATH=/var/task",
    ]
    if requirements_path:
        base_dockerfile_content.append(f"COPY {requirements_path} ./")
        base_dockerfile_content.append("RUN pip install -r requirements.txt")

    # Write the base Dockerfile
    base_dockerfile_path = os.path.join(dockerfiles_path, base_dockerfile_name)
    with open(base_dockerfile_path, "w") as file:
        file.write("\n".join(base_dockerfile_content))
    print(f"Base Dockerfile created at: {base_dockerfile_path}")
    for func in lambda_functions:
        handler_path = "handlers." + func._lambda_meta.get("handler")
        dockerfile_name = f"Dockerfile_{func._lambda_meta.get('name')}"

        dockerfile_content = [
            f"FROM {base_image} as base",
            f"FROM base",
            "WORKDIR /var/task",
            "COPY ./src ./",
            f'CMD ["{handler_path}"]',
        ]

        # Write the function-specific Dockerfile
        dockerfile_path = os.path.join(dockerfiles_path, dockerfile_name)
        with open(dockerfile_path, "w") as file:
            file.write("\n".join(dockerfile_content))
        print(
            f"Dockerfile for {func._lambda_meta.get('name')} created at: {dockerfile_path}"
        )


def build_and_push_images(
    lambda_functions, source_path, repository_name_base, tag="latest"
):
    client = docker.from_env()
    ecr_client = boto3.client("ecr")
    account_id = boto3.client("sts").get_caller_identity().get("Account")
    region = boto3.session.Session().region_name

    # Build the base image first
    base_image_tag = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name_base}_base:{tag}"
    client.images.build(
        path=source_path,
        dockerfile=f"{source_path}/dockerfiles/Dockerfile_base",
        tag=base_image_tag,
        rm=True,
    )
    client.images.push(base_image_tag)

    # Now build and push images for each function
    image_uris = []
    for func in lambda_functions:
        repository_name = f"{repository_name_base}_{func._lambda_meta.get('name').lower().replace(' ', '_')}"
        image_tag = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{tag}"

        # Ensure the repository exists
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

        # Build and push the Docker image
        dockerfile_path = (
            f"./dockerfiles/Dockerfile_{func._lambda_meta.get('name')}"
        )
        image, _ = client.images.build(
            path=source_path,
            dockerfile=dockerfile_path,
            tag=image_tag,
            rm=True,
            buildargs={"BASE_IMAGE": base_image_tag},
            # Pass the base image tag as a build arg
        )
        client.images.push(image_tag)
        image_uris.append(image_tag)

    return image_uris
