from django.core.mail import send_mail
import os

def send_otp_email(email, otp):
    send_mail(
        subject="Your OTP Code",
        message=f"Sizning OTP kodingiz: {otp}",
        from_email=os.getenv("EMAIL_HOST_USER"),
        recipient_list=[email],
        fail_silently=False,
    )