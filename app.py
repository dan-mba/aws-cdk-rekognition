#!/usr/bin/env python3

from aws_cdk import App

from aws_cdk_rekognition.aws_cdk_rekognition_stack import AwsCdkRekognitionStack

app = App()
AwsCdkRekognitionStack(app, "aws-cdk-rekognition")

app.synth()
