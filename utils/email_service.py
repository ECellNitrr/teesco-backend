from celery import shared_task
from decouple import config
from django.core.mail import EmailMessage
from decouple import config


@shared_task
def send_email(recipient,subject,body):
    if config('MOCK_EMAIL', cast=bool, default=True):
        print('Mock email service:')
        print('Subject:',subject)
        print('Recipients:',', '.join(recipient))
        print('Subject:',subject)
    else:
        msg = EmailMessage(subject, body, config('EMAIL_HOST_USER') , recipient)
        msg.content_subtype = "html"  
        msg.send()