import random
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from django.contrib.auth.hashers import make_password
from .utils.email import send_otp_email


from .redis_client import redis_client



class RegisterAPIView(APIView):

    def post(self, request):
        email = request.data.get("email")
        name = request.data.get("name")

        otp = str(random.randint(1000, 9999))

        redis_client.set(f"otp:{email}", otp, ex=120)

        # 🔥 REAL EMAIL SEND
        send_otp_email(email, otp)

        return Response({
            "message": "OTP sent to email"
        })


class VerifyOTPAPIView(APIView):

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"error": "email and otp required"}, status=400)

        saved_otp = redis_client.get(f"otp:{email}")

        if not saved_otp:
            return Response({"error": "OTP expired or not found"}, status=400)

        if saved_otp != otp:
            return Response({"error": "Invalid OTP"}, status=400)

        # 🔥 OTP ishlatildi → delete
        redis_client.delete(f"otp:{email}")

        # 🔥 user already exists check
        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=400)

        # 🔥 password generate
        raw_password = str(random.randint(100000, 999999))

        user = User.objects.create(
            name=email.split("@")[0],
            email=email,
            password=make_password(raw_password),
            tg_id="auto"
        )

        return Response({
            "message": "OTP verified, user created",
            "email": email,
            "password": raw_password
        })  


