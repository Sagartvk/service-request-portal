import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('service_requests')

def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response.get('Items', [])

        # Sort by created_at descending (newest first)
        items.sort(key=lambda x: x.get('created_at', ''), reverse=True)

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps(items)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
