import random
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from src.apps.users.models import User
from src.apps.users.utils.email import send_otp_email
from src.apps.users.redis_client import redis_client


class RegisterAPIView(APIView):

    def post(self, request):
        email = request.data.get("email")
        name = request.data.get("name")

        if not email or not name:
            return Response({"error": "email and name are required"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=400)

        otp = str(random.randint(1000, 9999))
        raw_password = str(random.randint(100000, 999999))

        user = User.objects.create(
            name=name,
            email=email,
            password=make_password(raw_password)
        )

        redis_client.set(f"otp:{email}", otp, ex=120)
        send_otp_email(email, otp)

        return Response({
            "message": "OTP sent to email and user created",
            "email": email,
            "password": raw_password
        }, status=201)
