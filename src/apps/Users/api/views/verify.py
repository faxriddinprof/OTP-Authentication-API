import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from src.apps.users.redis_client import redis_client
from src.apps.users.models import User
from src.apps.users.utils.otp import get_otp, delete_otp


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

        # Compare OTPs
        if saved_otp != str(otp):
            return Response({"error": "Invalid OTP"}, status=400)
        
        # Parse user data
        try:
            user_data = json.loads(user_data)
        except (json.JSONDecodeError, TypeError):
            return Response({"error": "Invalid user data"}, status=400)

        # Check if user already exists
        if User.objects.filter(email=user_data["email"]).exists():
            return Response({"error": "User already exists"}, status=400)

        # Create user
        try:
            user = User.objects.create(
                name=user_data["name"],
                email=user_data["email"],
                password=make_password(user_data["password"])
            )
        except KeyError:
            return Response({"error": "Invalid user data format"}, status=400)
        except Exception as e:
            return Response({"error": f"Error creating user: {str(e)}"}, status=500)

        # Clean up Redis data
        redis_client.delete(f"user_data:{email}")
        redis_client.delete(f"otp:{email}")
        redis_client.delete(f"resend_count:{email}")
        redis_client.delete(f"resend_lock:{email}")
    
        return Response({
            "message": "OTP verified successfully. User created",
            "user_id": user.id,
            "email": user.email
        }, status=201)
