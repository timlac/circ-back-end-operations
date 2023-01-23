from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_apigateway as apigateway
    # aws_sqs as sqs,
)
from constructs import Construct


class DbApiStack(Stack):
    db_table_name = "video_validation_experiment"
    db_index_name = "processed_index"

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a new Lambda function for the base path response
        base_path_handler = _lambda.Function(self, "BasePathFunction",
                                             runtime=_lambda.Runtime.PYTHON_3_7,
                                             handler="base_path.handler",
                                             code=_lambda.Code.from_asset("lambda"),
                                             )

        # Define a Lambda function for read operation
        read_fn = _lambda.Function(
            self, "ReadFunction",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="read.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE": self.db_table_name
            }
        )
        # Grant write permissions to the Lambda function
        update_policy = iam.PolicyStatement(
            actions=["dynamodb:GetItem", "dynamodb:Query"],
            resources=[f"arn:aws:dynamodb:{self.region}:{self.account}:table/{self.db_table_name}/index/*"]
        )
        read_fn.add_to_role_policy(update_policy)

        ####
        # Define a Lambda function for update operation
        update_fn = _lambda.Function(
            self, "UpdateFunction",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="update.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "DYNAMODB_TABLE": self.db_table_name
            }
        )
        # Grant write permissions to the Lambda function
        update_policy = iam.PolicyStatement(
            actions=["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:UpdateItem", "dynamodb:DeleteItem"],
            resources=[f"arn:aws:dynamodb:{self.region}:{self.account}:table/{self.db_table_name}"]
        )
        update_fn.add_to_role_policy(update_policy)

        ####
        # Define an API Gateway REST API
        api = apigateway.RestApi(self, "MyApi",
                                 deploy=True, )

        # Add a GET method to the base path resource
        api.root.add_method("GET", apigateway.LambdaIntegration(base_path_handler))

        # Define a resource for the API
        resource = api.root.add_resource("items")

        # Define a GET method for the resource, connected to the read Lambda function
        read_integration = apigateway.LambdaIntegration(read_fn)
        resource.add_method("GET", read_integration)

        # Define a PUT method for the resource, connected to the update Lambda function
        update_integration = apigateway.LambdaIntegration(update_fn)
        resource.add_method("PUT", update_integration)
