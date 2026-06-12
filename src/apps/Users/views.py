from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer
from .utils import generate_otp
from .redis_client import redis_client

class RegisterAPIView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        otp = generate_otp()

        redis_client.set(
            f"otp:{email}",
            otp,
            ex=120
        )

        return Response(
            {
                "message": "OTP generated",
                "otp": otp
            },
            status=status.HTTP_200_OK
        )