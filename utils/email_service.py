from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
import boto3


@shared_task
def send_email(recipient, subject, body):
    if settings.MOCK_EMAIL:

        print('Mock email service:')
        print(f'Recipients: {recipient}')
        print(f'Subject: {subject}')
        print(f'Body: {body}')
    else:
        if settings.EMAIL_BACKEND == 'AWS-SES':
            client = boto3.client(
                'ses',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION_NAME
            )
            try:
                sender_email = settings.EMAIL_HOST_USER

                response = client.send_email(
                    Source=sender_email,
                    Destination={
                        'ToAddresses': recipient
                    },
                    Message={
                        'Subject': {
                            'Data': subject,
                        },
                        'Body': {
                            'Text': {
                                'Data': body,
                            },
                            'Html': {
                                'Data': '',
                            }
                        }
                    },
                )

        elif settings.EMAIL_BACKEND == 'DJANGO-SMTP':
            try:
                msg = EmailMessage(subject, body, settings.EMAIL_HOST_USER, recipient)
                msg.content_subtype = "html"

                msg.send()
            except:
                raise ValueError("Invalid Gmail credentials.")
