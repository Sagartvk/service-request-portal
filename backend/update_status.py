import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('service_requests')

VALID_STATUSES = ['Pending', 'In Progress', 'Resolved']

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        request_id = body.get('request_id')
        new_status  = body.get('status')

        if not request_id or not new_status:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'request_id and status are required'})
            }

        if new_status not in VALID_STATUSES:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': f'status must be one of {VALID_STATUSES}'})
            }

        table.update_item(
            Key={'request_id': request_id},
            UpdateExpression='SET #s = :s',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':s': new_status}
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({'message': 'Status updated', 'request_id': request_id, 'status': new_status})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
