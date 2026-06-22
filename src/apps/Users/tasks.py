import logging
from celery import shared_task
from src.apps.users.utils.email import send_otp_email

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def send_otp_task(self, email, otp):
    try:
        send_otp_email(email, otp)
    except Exception as exc:
        logger.error("Failed to send OTP to %s: %s", email, exc)
        raise self.retry(exc=exc)