from constructs import Construct

from aws_cdk import (
    aws_lambda as _lambda,
    aws_iam as iam
)


class UpdateExperimentTable(Construct):

    def __init__(self, scope: Construct, id: str, db_table: str):
        super().__init__(scope, id)

        ####
        # Define a Lambda function for update operation
        self.lambda_fn = _lambda.Function(
            self, id,
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="update_experiment_table_lambda.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE": db_table
            }
        )
        # Grant write permissions to the Lambda function
        update_policy = iam.PolicyStatement(
            actions=["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:UpdateItem", "dynamodb:DeleteItem"],
            resources=[f"arn:aws:dynamodb:{scope.region}:{scope.account}:table/{db_table}"]
        )
        self.lambda_fn.add_to_role_policy(update_policy)
