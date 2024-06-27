from django.core.mail import send_mail
from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_activation_code(email, activation_code):
    user = User.objects.get(email=email)
    subject = 'Account Activation'
    message = f'Для активации вашего аккаунта, используйте следующий код: {activation_code}'
    send_mail(subject, message, 'admin@admin.com', [email])

@shared_task
def send_new_activation(email, activation_code):
    user = User.objects.get(email=email)
    subject = 'New Activation Code'
    message = f'Your new activation code is: {activation_code}'
    send_mail(subject, message, 'admin@admin.com', [email])
