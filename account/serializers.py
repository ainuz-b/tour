from rest_framework import serializers
from django.contrib.auth import get_user_model

from .tasks import send_activation_code, send_new_activation

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length = 4, required=True, write_only=True)

    class Meta:
        model = User 
        fields = 'email', 'password', 'password_confirm'

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпали!')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code(user.email, user.activation_code)
        return user 

class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    activation_code = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        activation_code = attrs.get('activation_code')
        user = User.objects.filter(email=email, activation_code=activation_code).exists()
        if not user:
            raise serializers.ValidationError('Неверный код активации или email!')
        return attrs

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с таким email не найден!')
        return value

    def send_new_activation(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_new_activation(user.email, user.activation_code)

    
    def create_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(min_length=4, required=True)
    new_password_confirm = serializers.CharField(min_length=4, required=True)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Неверный старый пароль!')
        return old_password

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': 'Новые пароли не совпадают!'})
        return attrs

    def change_password(self):
        new_password = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()
