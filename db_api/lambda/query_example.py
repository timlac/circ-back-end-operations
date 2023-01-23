import json
import boto3
import os
from decimal import Decimal


# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')


def to_serializable(val):
    if isinstance(val, Decimal):
        return str(val)
    return val


def handler(event, context):
    try:
        table_name = os.environ["DYNAMODB_TABLE"]
        table = dynamodb.Table(table_name)

        # Get query parameters from the event
        example_number = event['queryStringParameters']['example_number']
        valence = event['queryStringParameters']['valence']

        # Query the table
        response = table.query(
            KeyConditionExpression='example_number = :ex and valence = :v',
            ExpressionAttributeValues={
                ':ex': int(example_number),
                ':v': valence
            }
        )

        # Return the query result
        return {
            "statusCode": 200,
            "body": json.dumps(response['Items'], default=to_serializable)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
