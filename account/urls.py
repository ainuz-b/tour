from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, ActivationView, PasswordResetView, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('resetpassword/', PasswordResetView.as_view()),
    path('changepassword/', ChangePasswordView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]