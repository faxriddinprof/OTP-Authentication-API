from django.urls import path
from .views.register import RegisterAPIView
from .views.verify import VerifyOTPAPIView
from .views.login import LoginAPIView
from .views.logout import LogoutAPIView 

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("verify/", VerifyOTPAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("logout/", LogoutAPIView.as_view()),
]