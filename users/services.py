from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


def send_verification_code(verification_code, email):
    url = reverse('users:verification', args=[verification_code])
    send_mail(
        subject='Регистрация на VaGon 2.0',
        message=f'Для регистрации на платформе VaGon 2.0 пройдите по ссылке {"http://127.0.0.1:8000" + url}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )


def send_new_password(new_password, email):
    send_mail(
        subject='Смена пароля на платформе VaGon 2.0',
        message=f'Ваш новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
