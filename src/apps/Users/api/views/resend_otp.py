from rest_framework.views import APIView
from rest_framework.response import Response

from src.apps.users.redis_client import redis_client
from src.apps.users.tasks import send_otp_task

from src.apps.users.utils.otp import (
    create_otp,
    get_resend_count,
    increment_resend_count,
    has_resend_lock,
    set_resend_lock
)


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
                {"error": "Registration expired"},
                status=400
            )

        if has_resend_lock(email):
            return Response(
                {"error": "Wait 30 seconds before requesting again"},
                status=429
            )

        resend_count = get_resend_count(email)

        if resend_count >= 3:
            return Response(
                {"error": "Maximum resend attempts reached"},
                status=429
            )

        otp = create_otp(email)

        increment_resend_count(email)

        set_resend_lock(email)

        send_otp_task.delay(
            email,
            otp
        )

        return Response({
            "message": "OTP sent again"
        })