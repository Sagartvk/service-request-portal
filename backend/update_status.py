import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('service_requests')
sns      = boto3.client('sns', region_name=os.environ.get('AWS_REGION', 'us-east-2'))

SNS_TOPIC_ARN  = os.environ.get('SNS_TOPIC_ARN', '')
VALID_STATUSES = ['Pending', 'In Progress', 'Resolved']

STATUS_EMOJI = {
    'Pending':     '⏳',
    'In Progress': '🔄',
    'Resolved':    '✅'
}

def is_confirmed_subscriber(email):
    """Return True if email has a confirmed SNS subscription."""
    paginator = sns.get_paginator('list_subscriptions_by_topic')
    for page in paginator.paginate(TopicArn=SNS_TOPIC_ARN):
        for sub in page['Subscriptions']:
            if (sub['Protocol'] == 'email'
                    and sub['Endpoint'].lower() == email.lower()
                    and sub['SubscriptionArn'] != 'PendingConfirmation'):
                return True
    return False

def send_status_email(email, name, request_id, new_status, description):
    if not SNS_TOPIC_ARN or not email:
        return

    if not is_confirmed_subscriber(email):
        print(f"Email {email} not a confirmed subscriber — skipping notification")
        return

    emoji   = STATUS_EMOJI.get(new_status, '📋')
    subject = f"[ServiceDesk] {emoji} Your Request Status Updated – {request_id}"

    if new_status == 'In Progress':
        status_note = "Our team has picked up your request and is actively working on it."
    elif new_status == 'Resolved':
        status_note = "Great news! Your request has been resolved. Please check and confirm everything is working."
    else:
        status_note = "Your request is in the queue and will be reviewed shortly."

    message = f"""Hello {name},

Your service request status has been updated.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STATUS UPDATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Request ID   : {request_id}
Description  : {description}
New Status   : {emoji} {new_status}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{status_note}

You can track your request anytime using your Request ID.

ServiceDesk · IT Support Portal
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is an automated message. Please do not reply.
"""

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message
    )
    print(f"Status update email sent to {email} — status: {new_status}")


def lambda_handler(event, context):
    try:
        body       = json.loads(event['body'])
        request_id = body.get('request_id')
        new_status = body.get('status')

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

        # 1. Update status in DynamoDB
        table.update_item(
            Key={'request_id': request_id},
            UpdateExpression='SET #s = :s',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':s': new_status}
        )

        # 2. Fetch full item to get email, name, description
        response = table.get_item(Key={'request_id': request_id})
        item     = response.get('Item', {})

        # 3. Send email notification (non-blocking)
        try:
            send_status_email(
                email       = item.get('email'),
                name        = item.get('name', 'User'),
                request_id  = request_id,
                new_status  = new_status,
                description = item.get('description', '—')
            )
        except Exception as sns_error:
            print(f"SNS error (non-fatal): {sns_error}")

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({
                'message': 'Status updated',
                'request_id': request_id,
                'status': new_status
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
