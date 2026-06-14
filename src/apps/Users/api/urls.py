from django.urls import path
from .views.register import RegisterAPIView
from .views.verify import VerifyOTPAPIView
from .views.login import LoginAPIView
from .views.logout import LogoutAPIView 
from .views.resend_otp import ResendOTPAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("verify/", VerifyOTPAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("logout/", LogoutAPIView.as_view()),
    path("resend-otp/", ResendOTPAPIView.as_view()),
]