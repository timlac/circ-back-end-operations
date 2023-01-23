import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    try:

        table_name = os.environ["DYNAMODB_TABLE"]
        table = dynamodb.Table(table_name)

        # Get the 'alias', 'filename', and 'processed_status' from the request body
        body = json.loads(event["body"])
        alias = body["alias"]
        filename = body["filename"]
        processed_status = body["processed_status"]

        # Update the item in the table
        table.update_item(
            Key={
                "alias": alias,
                "filename": filename
            },
            UpdateExpression="SET processed_status = :s",
            ExpressionAttributeValues={
                ":s": int(processed_status)
            },
            ReturnValues="UPDATED_NEW"
        )

        # Return a success message
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item with filename {} updated successfully".format(filename)})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
