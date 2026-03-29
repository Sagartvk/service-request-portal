import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('service_requests')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        request_id = str(uuid.uuid4())[:8]

        item = {
            "request_id": request_id,
            "name": body["name"],
            "email": body["email"],
            "location": body["location"],
            "description": body["description"],
            "status": "OPEN"
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "request_id": request_id
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }
