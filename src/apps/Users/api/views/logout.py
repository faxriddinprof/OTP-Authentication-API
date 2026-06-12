from rest_framework.views import APIView
from rest_framework.response import Response

class LogoutAPIView(APIView):

    def post(self, request):
        request.session.flush()

        return Response({
            "message": "Logged out successfully"
        })