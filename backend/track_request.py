import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('service_requests')

def lambda_handler(event, context):
    try:
        # Get request_id from query string
        request_id = event['queryStringParameters']['request_id']

        response = table.get_item(
            Key={
                'request_id': request_id
            }
        )

        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'message': 'Request not found'})
            }

        item = response['Item']

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(item)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
