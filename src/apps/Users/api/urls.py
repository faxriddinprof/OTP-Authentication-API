from django.urls import path
from .views.register import RegisterAPIView
from .views.verify import VerifyOTPAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("verify/", VerifyOTPAPIView.as_view()),
]