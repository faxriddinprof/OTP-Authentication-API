import json
from rest_framework.views import APIView
from rest_framework.response import Response
from src.apps.users.models import User
from src.apps.users.redis_client import redis_client
from src.apps.users.tasks import send_otp_task
from src.apps.users.utils.otp import create_otp

class RegisterAPIView(APIView):

    def post(self, request):
        email = request.data.get("email")
        name = request.data.get("name")
        password = request.data.get("password")

        if not email or not name or not password:
            return Response({"error": "email, name, and password are required"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=400)

        if len(password) < 5:
            return Response({"error": "Password must be at least 5 characters long"}, status=400)

        otp = create_otp(email)

        redis_client.set(
            f"user_data:{email}",
            json.dumps({
                "name": name,
                "email": email,
                "password": password,
            }),
            ex=600
            )
        
        send_otp_task.delay(email, otp)


        return Response({
            "message": "OTP sent. Please verify your email",
        }, status=201)
