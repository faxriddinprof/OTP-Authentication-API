import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from src.apps.users.redis_client import redis_client
from src.apps.users.models import User
from src.apps.users.utils.otp import get_otp

class VerifyOTPAPIView(APIView):

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"error": "email and otp required"}, status=400)

        user_data = redis_client.get(f"user_data:{email}")
        if not user_data:
            return Response({"error": "User data not found"}, status=400)
        
        saved_otp = get_otp(email)
        
        if not saved_otp:
            return Response(
                {"error": "OTP expired"},
                status=400
            )

        if saved_otp != str(otp):
            return Response(
                {"error": "Invalid OTP"},
                status=400
            )
        
        user_data = json.loads(user_data)

        user = User.objects.create(
            name=user_data["name"],
            email=user_data["email"],
            password=make_password(user_data["password"])
        )

        redis_client.delete(f"resend_count:{email}")
        redis_client.delete(f"resend_lock:{email}") 
    
        return Response({
            "message": "OTP verified, user created",
        })
