from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway
)
from constructs import Construct

from .update_experiment_table import UpdateExperimentTable
from.query_processed_index import QueryProcessedIndex


class DbApiStack(Stack):
    db_table_name = "video_validation_experiment"

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a new Lambda function for the base path response
        base_path_handler = _lambda.Function(self, "BasePathFunction",
                                             runtime=_lambda.Runtime.PYTHON_3_7,
                                             handler="base_path.handler",
                                             code=_lambda.Code.from_asset("lambda"),
                                             )

        update_fn = UpdateExperimentTable(self, "UpdateFunction", self.db_table_name)
        read_fn = QueryProcessedIndex(self, "QueryProcessedIndexFunction", self.db_table_name)

        ####
        # Define an API Gateway REST API
        api = apigateway.RestApi(self, "video-validation-api",
                                 deploy=True, )

        # Add a GET method to the base path resource
        api.root.add_method("GET", apigateway.LambdaIntegration(base_path_handler))

        # Define a resource for the API
        resource = api.root.add_resource("items")

        # Define a GET method for the resource, connected to the read Lambda function
        read_integration = apigateway.LambdaIntegration(read_fn.lambda_fn)
        resource.add_method("GET", read_integration)

        # Define a PUT method for the resource, connected to the update Lambda function
        update_integration = apigateway.LambdaIntegration(update_fn.lambda_fn)
        resource.add_method("PUT", update_integration)
