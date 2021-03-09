#!/usr/bin/env python3

from aws_cdk import core as cdk

from aws_cdk_rekognition.aws_cdk_rekognition_stack import AwsCdkRekognitionStack

app = cdk.App()
AwsCdkRekognitionStack(app, "aws-cdk-rekognition")

app.synth()
