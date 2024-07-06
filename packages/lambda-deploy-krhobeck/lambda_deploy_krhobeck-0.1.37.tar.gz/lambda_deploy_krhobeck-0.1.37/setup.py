from setuptools import setup, find_packages

setup(
    name="lambda_deploy_krhobeck",
    version="0.1.37",
    packages=find_packages(),
    description="Makes AWS Lambda deployment more fluent",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Kyle Hobeck",
    author_email="krhobeck@gmail.com",
    url="https://github.com/krhobeck/lambda_deploy",
    install_requires=[
        "boto3",
        "moto",
        "pydantic",
        "flake8",
        "mypy",
        "mypy-boto3-apigateway",
        "mypy-boto3-iam",
        "mypy-boto3-lambda",
        "mypy-boto3-s3",
        "openapi_spec_validator",
        "docker",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "deploy_lambda=lambda_deploy_krhobeck.deployment:deploy",
        ],
    },
)
