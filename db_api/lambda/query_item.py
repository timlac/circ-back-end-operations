import boto3
import json
import os

from serializer import to_serializable

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    try:
        table_name = os.environ["DYNAMODB_TABLE"]
        table = dynamodb.Table(table_name)

        # Get the partition key value from the event
        partition_key_value = event['queryStringParameters']['alias']

        print("GET request for item {}".format(partition_key_value))

        # Query the table using the partition key
        response = table.query(
            KeyConditionExpression='alias = :alias_val',
            ExpressionAttributeValues={':alias_val': partition_key_value}
        )

        # Return the query result
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(response['Items'], default=to_serializable)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
