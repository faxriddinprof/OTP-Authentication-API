import random
from rest_framework.views import APIView
from rest_framework.response import Response
from src.apps.users.utils.email import send_otp_email
from src.apps.users.redis_client import redis_client


class RegisterAPIView(APIView):

    def post(self, request):
        email = request.data.get("email")
        name = request.data.get("name")

        otp = str(random.randint(1000, 9999))

        redis_client.set(f"otp:{email}", otp, ex=120)

        send_otp_email(email, otp)

        return Response({
            "message": "OTP sent to email"
        })
