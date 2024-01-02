from constructs import Construct
from aws_cdk import Stack, CfnOutput
from aws_cdk.aws_lambda import (
    Code,
    Function,
    Runtime,
    Architecture
)
from aws_cdk.aws_apigatewayv2_integrations import (
    HttpLambdaIntegration
)
from aws_cdk.aws_apigatewayv2 import (
    HttpApi,
    CorsPreflightOptions,
    HttpMethod,
    CorsHttpMethod
)
from aws_cdk.aws_iam import (
    PolicyStatement,
    Effect
)


class AwsCdkRekognitionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        rekLambda = Function(self, "REK_LAMBDA",
                             runtime=Runtime.PYTHON_3_11,
                             code=Code.from_asset("./rek_lambda"),
                             handler="app.handler",
                             architecture=Architecture.ARM_64,
                             )

        rekLambda.add_to_role_policy(
            PolicyStatement(
                effect=Effect.ALLOW,
                actions=["rekognition:DetectLabels"],
                resources=["*"]
            )
        )

        rekInt = HttpLambdaIntegration("LambdaProxyIntegration", handler=rekLambda)

        rekAPI = HttpApi(self, "LABELS_API",
                         cors_preflight=CorsPreflightOptions(
                             allow_headers=["content-type"],
                             allow_methods=[
                                 CorsHttpMethod.OPTIONS, CorsHttpMethod.POST],
                             allow_origins=[
                                 "http://localhost:3000", "https://dan-mba.github.io"]
                         )
                         )

        rekAPI.add_routes(
            path="/labels",
            methods=[HttpMethod.OPTIONS, HttpMethod.POST],
            integration=rekInt
        )

        CfnOutput(self, "URL",
                  value=f"{rekAPI.url}labels",
                  description="API url"
                  )
