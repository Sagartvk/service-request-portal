import json
import boto3
import uuid
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('service_requests')

sns      = boto3.client('sns', region_name=os.environ.get('AWS_REGION', 'us-east-2'))

# SNS Topic ARN — set this as a Lambda environment variable: SNS_TOPIC_ARN
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')

def send_confirmation_email(email, name, request_id, description, location):
    """Subscribe the user's email to the SNS topic and publish confirmation."""
    if not SNS_TOPIC_ARN:
        print("SNS_TOPIC_ARN not set, skipping email")
        return

    # Subscribe user email to the topic (no-op if already subscribed)
    sns.subscribe(
        TopicArn=SNS_TOPIC_ARN,
        Protocol='email',
        Endpoint=email,
        Attributes={
            'FilterPolicy': json.dumps({'request_id': [request_id]})
        }
    )

    subject = f"[ServiceDesk] Request Received – ID: {request_id}"

    message = f"""Hello {name},

Your service request has been successfully submitted.

──────────────────────────────────
  REQUEST DETAILS
──────────────────────────────────
  Request ID  : {request_id}
  Name        : {name}
  Location    : {location or 'Not specified'}
  Description : {description}
  Status      : Pending
  Submitted   : {datetime.utcnow().strftime('%d %b %Y, %H:%M UTC')}
──────────────────────────────────

Please save your Request ID — you'll need it to track your request status.

Track your request here:
https://your-portal-url/track.html

Our team will review your request and get back to you shortly.

──────────────────────────────────
ServiceDesk · IT Support Portal
© 2025 ServiceDesk. All rights reserved.
──────────────────────────────────

This is an automated message. Please do not reply to this email.
"""

    # Publish to SNS — targets only this email via filter policy
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message,
        MessageAttributes={
            'request_id': {
                'DataType': 'String',
                'StringValue': request_id
            }
        }
    )


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

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

        # 2. Send confirmation email via SNS (non-blocking — won't fail the request)
        try:
            if email:
                send_confirmation_email(email, name, request_id, description, location)
        except Exception as sns_error:
            # Log SNS error but don't fail the whole request
            print(f"SNS error (non-fatal): {sns_error}")

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
