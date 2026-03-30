import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('service_requests')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        name = body.get('name')
        location = body.get('location')
        description = body.get('description')
        email = body.get('email')

        request_id = str(uuid.uuid4())[:8]   # shorter ID

        item = {
            'request_id': request_id,
            'name': name,
            'location': location,
            'description': description,
            'email': email,
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
