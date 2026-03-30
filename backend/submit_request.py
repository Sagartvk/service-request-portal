import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ServiceRequests')  # make sure table name matches

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        name = body.get('name')
        location = body.get('location')

        if not name or not location:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Missing name or location'})
            }

        request_id = str(uuid.uuid4())

        item = {
            'request_id': request_id,
            'name': name,
            'location': location,
            'status': 'Pending',
            'created_at': datetime.utcnow().isoformat()
        }

        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Request submitted successfully',
                'request_id': request_id
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
