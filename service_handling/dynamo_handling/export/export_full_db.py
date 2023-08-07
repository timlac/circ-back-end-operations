from config import experiment_table_name

import boto3
from decimal import Decimal
import json
import pandas as pd

def to_serializable(val):
    if isinstance(val, Decimal):
        return str(val)
    return val

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(experiment_table_name)

def scan_table(table, limit=None):
    items = []
    response = table.scan()
    items += response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items += response['Items']

    return items


items = scan_table(table)
items_json = json.dumps(items, default=to_serializable)
df = pd.read_json(items_json)

df.to_csv("full_export.csv", index=False)

# df = df[["alias", "valence", "set_number", "randomization_id"]]
#
# df2 = df.drop_duplicates(subset="alias", keep="first")
# df2.sort_values(by=["set_number", "randomization_id"], inplace=True)
# df2.to_csv("aliases.csv", index=False)
