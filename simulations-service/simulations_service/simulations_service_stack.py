from aws_cdk import core
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_lambda as lam

class SimulationsServiceStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
