import json
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from src.apps.users.models import User
from src.apps.users.redis_client import redis_client
from src.apps.users.tasks import send_otp_task
from src.apps.users.utils.otp import create_otp
from src.apps.users.serializer.register import RegisterSerializer


class RegisterRateThrottle(AnonRateThrottle):
    rate = '5/hour'


class RegisterAPIView(APIView):
    throttle_classes = [RegisterRateThrottle]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = serializer.validated_data["email"]
        name = serializer.validated_data["name"]
        password = serializer.validated_data["password"]

        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=400)

        otp = create_otp(email)

        redis_client.set(
            f"user_data:{email}",
            json.dumps({
                "name": name,
                "email": email,
                "password": make_password(password),
            }),
            ex=600
        )

        send_otp_task.delay(email, otp)

        return Response({
            "message": "OTP sent. Please verify your email",
        }, status=201)
