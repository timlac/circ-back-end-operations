import boto3
from pprint import pprint

from botocore.exceptions import ClientError

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')

table_name = "example_videos"
table = dynamodb.Table(table_name)

# Get query parameters from the event
example_number = 0
valence = "kiss"
emotion_id = 1000
filename = "new filename"
video_id = "A1000"

try:
    # Update the item in the table
    response = table.update_item(
        Key={
            "example_number": example_number,
            "valence": valence
        },
        UpdateExpression="SET emotion_id = :e, filename = :f, video_id = :v",
        ConditionExpression="attribute_exists(example_number) "
                            "AND attribute_exists(valence)",
        ExpressionAttributeValues={
            ":e": emotion_id,
            ":f": filename,
            ":v": video_id

        },
        ReturnValues="UPDATED_NEW"
    )
    pprint(response)
except ClientError as e:
    if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
        print("Primary key does not exist.")
    else:
        print(e)
        raise
