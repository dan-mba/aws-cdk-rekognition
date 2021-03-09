from aws_cdk import core as cdk
from aws_cdk.aws_lambda import (
    Code,
    Function,
    Runtime
)
from aws_cdk.aws_apigatewayv2_integrations import (
    LambdaProxyIntegration
)
from aws_cdk.aws_apigatewayv2 import (
    HttpApi,
    CorsPreflightOptions,
    HttpMethod
)
from aws_cdk.aws_iam import (
    PolicyStatement,
    Effect
)


class AwsCdkRekognitionStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        rekLambda = Function(self, "REK_LAMBDA",
                             runtime=Runtime.PYTHON_3_8,
                             code=Code.from_asset("./rek_lambda"),
                             handler="app.handler"
                             )

        rekLambda.add_to_role_policy(
            PolicyStatement(
                effect=Effect.ALLOW,
                actions=["rekognition:DetectLabels"],
                resources=["*"]
            )
        )

        rekInt = LambdaProxyIntegration(handler=rekLambda)

        rekAPI = HttpApi(self, "LABELS_API",
                         cors_preflight=CorsPreflightOptions(
                             allow_headers=["content-type"],
                             allow_methods=[
                                 HttpMethod.OPTIONS, HttpMethod.POST],
                             allow_origins=[
                                 "http://localhost:3000", "https://dan-mba.github.io"]
                         )
                         )

        rekAPI.add_routes(
            path="/labels",
            methods=[HttpMethod.OPTIONS, HttpMethod.POST],
            integration=rekInt
        )

        cdk.CfnOutput(self, "URL",
                      value=f"{rekAPI.url}labels",
                      description="API url"
                      )
