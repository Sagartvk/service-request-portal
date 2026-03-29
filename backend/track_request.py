import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('service_requests')

def lambda_handler(event, context):
    request_id = event['queryStringParameters']['id']

    res = table.get_item(Key={"request_id": request_id})

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(res.get("Item", {}))
    }
