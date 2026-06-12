import random
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from src.apps.users.redis_client import redis_client
from src.apps.users.models import User


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

        redis_client.delete(f"otp:{email}")

        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=400)

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
