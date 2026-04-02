import json
import boto3
import uuid
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('service_requests')
sns      = boto3.client('sns', region_name=os.environ.get('AWS_REGION', 'us-east-2'))

# Set this as Lambda env variable: SNS_TOPIC_ARN
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')

def is_already_confirmed(email):
    """Check if email is already a confirmed subscriber on the topic."""
    paginator = sns.get_paginator('list_subscriptions_by_topic')
    for page in paginator.paginate(TopicArn=SNS_TOPIC_ARN):
        for sub in page['Subscriptions']:
            if sub['Protocol'] == 'email' and sub['Endpoint'].lower() == email.lower():
                # PendingConfirmation means not confirmed yet
                if sub['SubscriptionArn'] != 'PendingConfirmation':
                    return True
    return False

def send_confirmation_email(email, name, request_id, description, location):
    if not SNS_TOPIC_ARN:
        print("SNS_TOPIC_ARN not set, skipping email")
        return

    already_confirmed = is_already_confirmed(email)

    if not already_confirmed:
        # Subscribe the email — user will get a confirmation email from AWS first
        sns.subscribe(
            TopicArn=SNS_TOPIC_ARN,
            Protocol='email',
            Endpoint=email
            # NO FilterPolicy here — keep it simple
        )
        print(f"Subscribed {email} — awaiting confirmation")
        # Can't send message yet since subscription is pending
        # The actual notification will be sent on next submit after confirmation
        return

    # Email is confirmed — publish directly via SNS
    subject = f"[ServiceDesk] Request Received – ID: {request_id}"
    message = f"""Hello {name},

Your service request has been successfully submitted to ServiceDesk.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REQUEST DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Request ID   : {request_id}
Name         : {name}
Location     : {location or 'Not specified'}
Description  : {description}
Status       : Pending
Submitted at : {datetime.utcnow().strftime('%d %b %Y, %H:%M UTC')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Save your Request ID — you will need it to track your request.

Our support team will review and respond shortly.

ServiceDesk · IT Support Portal
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is an automated message. Please do not reply.
"""

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message
    )
    print(f"Confirmation email published to {email}")


def lambda_handler(event, context):
    try:
        body        = json.loads(event['body'])
        name        = body.get('name')
        location    = body.get('location')
        description = body.get('description')
        email       = body.get('email')

        request_id = str(uuid.uuid4())[:8]

        item = {
            'request_id': request_id,
            'name':        name,
            'location':    location,
            'description': description,
            'email':       email,
            'status':      'Pending',
            'created_at':  datetime.utcnow().isoformat()
        }

        # 1. Save to DynamoDB
        table.put_item(Item=item)

        # 2. Send email via SNS (non-blocking)
        try:
            if email:
                send_confirmation_email(email, name, request_id, description, location)
        except Exception as sns_error:
            print(f"SNS error (non-fatal): {sns_error}")

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'Request submitted successfully',
                'request_id': request_id
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
