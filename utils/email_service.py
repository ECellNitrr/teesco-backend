from celery import shared_task
from django.core.mail import send_mail
from decouple import config

@shared_task
def send_email(recipient,subject,body):
    send_mail(subject, body, config('EMAIL_HOST_USER') , recipient)
