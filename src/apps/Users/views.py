import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .redis_client import redis_client


class RegisterAPIView(APIView):

    def post(self, request):
        email = request.data.get("email")
        name = request.data.get("name")

        if not email or not name:
            return Response(
                {"error": "email and name required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # OTP generate
        otp = str(random.randint(1000, 9999))

        # Redisga yozish (120 sekund)
        redis_client.set(
            f"otp:{email}",
            otp,
            ex=120
        )

        return Response({
            "message": "OTP sent (simulated)",
            "otp": otp  # TEMPORARY (keyin o‘chiramiz)
        })
    

class VerifyOTPAPIView(APIView):

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        saved_otp = redis_client.get(f"otp:{email}")

        if not saved_otp:
            return Response(
                {"error": "OTP expired or not found"},
                status=400
            )

        if saved_otp != otp:
            return Response(
                {"error": "Invalid OTP"},
                status=400
            )

        # OTP success → delete
        redis_client.delete(f"otp:{email}")

        return Response({
            "message": "OTP verified successfully"
        })