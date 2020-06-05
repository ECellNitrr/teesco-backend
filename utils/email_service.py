from celery import shared_task
from decouple import config
from django.core.mail import EmailMessage, send_mail
import boto3


@shared_task
def send_email(recipient, subject, body):
    if config('MOCK_EMAIL', cast=bool):
        print('Mock email service:')
        print(f'Recipients: {recipient}')
        print(f'Subject: {subject}')
        print(f'Body: {body}')
    else:
        if config('EMAIL_BACKEND', cast=str) == 'django_amazon_ses.EmailBackend':
            client = boto3.client(
                'ses',
                aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
                region_name=config('AWS_REGION_NAME')
            )
            try:
                sender_email = config('EMAIL_HOST_USER')
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
            except:
                raise ValueError("Invalid SES credentials.")

        elif config('EMAIL_BACKEND', cast=str) == 'django.core.mail.backends.smtp.EmailBackend':
            try:
                msg = EmailMessage(subject, body, config(
                    'EMAIL_HOST_USER'), recipient)
                msg.content_subtype = "html"
                msg.send()
            except:
                raise ValueError("Invalid Gmail credentials.")
