#!/usr/bin/env python3
import aws_cdk as cdk
from app_stack import LambdaDeployStack


app = cdk.App()
LambdaDeployStack(
    app,
    "LambdaDeployStack",
)

app.synth()
