from celery import shared_task
from src.apps.users.utils.email import send_otp_email


@shared_task
def send_otp_task(email, otp):
    send_otp_email(email, otp)