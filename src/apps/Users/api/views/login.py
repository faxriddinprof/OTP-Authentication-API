from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from src.apps.users.models import User


class LoginAPIView(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if not check_password(password, user.password):
            return Response({"error": "Wrong password"}, status=400)

        request.session["user_id"] = user.id

        return Response({
            "message": "Login successful"
        })