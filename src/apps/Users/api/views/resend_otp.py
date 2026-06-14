from rest_framework.views import APIView
from rest_framework.response import Response

from src.apps.users.redis_client import redis_client
from src.apps.users.tasks import send_otp_task
from src.apps.users.utils.otp import create_otp


class ResendOTPAPIView(APIView):

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"error": "email required"},
                status=400
            )

        user_data = redis_client.get(
            f"user_data:{email}"
        )

        if not user_data:
            return Response(
                {"error": "OTP expired"}
            )

        otp = create_otp(email)

        send_otp_task.delay(
            email,
            otp
        )

        return Response({
            "message": "OTP sent again"
        })