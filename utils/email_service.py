from celery import shared_task
from decouple import config
from django.core.mail import EmailMessage


@shared_task
def send_email(recipient,subject,body):
    msg = EmailMessage(subject, body, config('EMAIL_HOST_USER') , recipient)
    msg.content_subtype = "html"  
    msg.send()
