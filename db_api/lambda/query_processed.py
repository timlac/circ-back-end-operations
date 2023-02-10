import json
import boto3
import os

from serializer import to_serializable

dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    try:

        table_name = os.environ["DYNAMODB_TABLE"]
        table = dynamodb.Table(table_name)

        # Get the 'alias' and 'processed_status' from the query string parameters
        alias = event["queryStringParameters"]["alias"]
        processed_status = event["queryStringParameters"]["processed_status"]

        print("GET request for item with alias: {}, and processed_status: {}".format(alias, processed_status))

        # Get the items from the table using the index
        response = table.query(
            IndexName="processed_index",
            KeyConditionExpression="alias = :a and processed_status = :s",
            ExpressionAttributeValues={
                ":a": alias,
                ":s": int(processed_status)
            }
        )
        items = response["Items"]

        # Return the items in the response
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(items, default=to_serializable)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
