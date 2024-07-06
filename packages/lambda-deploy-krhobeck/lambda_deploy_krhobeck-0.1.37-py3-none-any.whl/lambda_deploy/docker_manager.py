import base64

import boto3
import docker


def generate_dockerfile(base_image, requirements_path=None, copy_paths=None):
    dockerfile_content = [f"FROM {base_image}", "WORKDIR /app"]

    if requirements_path:
        dockerfile_content.append(f"COPY {requirements_path} ./")
        dockerfile_content.append("RUN pip install -r requirements.txt")

    if copy_paths:
        for path in copy_paths:
            dockerfile_content.append(f"COPY {path} ./")

    dockerfile_content.append(
        'CMD ["handler.lambda_handler"]'
    )  # Customize handler

    dockerfile_path = "Dockerfile"
    with open(dockerfile_path, "w") as file:
        file.write("\n".join(dockerfile_content))

    return dockerfile_path


def build_and_push_image(source_path, repository_name, tag="latest"):
    client = docker.from_env()
    ecr_client = boto3.client("ecr")
    account_id = boto3.client("sts").get_caller_identity().get("Account")
    region = boto3.session.Session().region_name
    image_tag = (
        f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{tag}"
    )

    # Ensure repository exists
    try:
        ecr_client.create_repository(repositoryName=repository_name)
    except ecr_client.exceptions.RepositoryAlreadyExistsException:
        pass

    # Authenticate to ECR
    token = ecr_client.get_authorization_token()
    username, password = (
        base64.b64decode(token["authorizationData"][0]["authorizationToken"])
        .decode()
        .split(":")
    )
    registry = token["authorizationData"][0]["proxyEndpoint"]
    client.login(username, password, registry=registry)

    # Build and push the Docker image
    image, _ = client.images.build(path=source_path, tag=image_tag, rm=True)
    client.images.push(image_tag)

    return image_tag
