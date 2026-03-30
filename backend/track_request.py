import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('service_requests')

def lambda_handler(event, context):
    try:
        params = event.get('queryStringParameters', {})

        # accept both id and request_id
        request_id = params.get('request_id') or params.get('id')

        if not request_id:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Missing request_id'})
            }

        response = table.get_item(
            Key={'request_id': request_id}
        )

        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'message': 'Request not found'})
            }

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(response['Item'])
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
