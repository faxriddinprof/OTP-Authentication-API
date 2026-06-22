import json
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from src.apps.users.redis_client import redis_client
from src.apps.users.models import User
from src.apps.users.utils.otp import (
    get_otp,
    get_otp_attempts,
    increment_otp_attempts,
    delete_otp_attempts,
)


class VerifyOTPAPIView(APIView):

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"error": "email and otp are required"}, status=400)

        # Get user_data from Redis
        user_data = redis_client.get(f"user_data:{email}")
        if not user_data:
            return Response({"error": "User data not found. Please register again"}, status=400)

        # Get saved OTP
        saved_otp = get_otp(email)
        if not saved_otp:
            return Response({"error": "OTP expired. Please request a new OTP"}, status=400)

        # Check attempt limit before comparing
        if get_otp_attempts(email) >= 5:
            return Response({"error": "Too many failed attempts. Please request a new OTP"}, status=429)

        # Compare OTPs
        if saved_otp != str(otp):
            increment_otp_attempts(email)
            return Response({"error": "Invalid OTP"}, status=400)

        # Parse user data
        try:
            user_data = json.loads(user_data)
        except (json.JSONDecodeError, TypeError):
            return Response({"error": "Invalid user data"}, status=400)

        # Create user (password is already hashed in Redis)
        try:
            user = User.objects.create(
                name=user_data["name"],
                email=user_data["email"],
                password=user_data["password"],
            )
        except IntegrityError:
            return Response({"error": "User already exists"}, status=400)
        except KeyError:
            return Response({"error": "Invalid user data format"}, status=400)

        # Clean up Redis data
        redis_client.delete(f"user_data:{email}")
        redis_client.delete(f"otp:{email}")
        redis_client.delete(f"resend_count:{email}")
        redis_client.delete(f"resend_lock:{email}")
        delete_otp_attempts(email)

        return Response({
            "message": "OTP verified successfully. User created",
            "user_id": user.id,
            "email": user.email
        }, status=201)
