from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model 
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterSerializer, ActivationSerializer, PasswordResetSerializer, ChangePasswordSerializer

User = get_user_model()

class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response('Вы успешно зарегистрировались!', 201)

class ActivationView(APIView):
    @swagger_auto_schema(request_body=ActivationSerializer())
    def get(self, request, email, activation_code):
        user = User.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response('Пользователь не найден', 404)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Вы успешно активировали акаунт', 200)
    
    
class PasswordResetView(APIView):
    @swagger_auto_schema(request_body=PasswordResetSerializer())
    def post(self, request):
        data = request.data
        serializer = PasswordResetSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_new_activation()
        return Response('Инструкции по сбросу пароля отправлены на ваш email.', 200)
    
class ChangePasswordView(APIView):
    @swagger_auto_schema(request_body=ChangePasswordSerializer())
    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.change_password()
        return Response('Пароль успешно изменен!', 200)