import random
import secrets

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:index')  # можно бы перекинуть на страницу с уведомлением о том, что нужно почту проверить

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            # verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            verification_code = secrets.token_urlsafe(nbytes=8)
            self.object.verification_code = verification_code
            self.object.is_active = False
            self.object = form.save()
            url = reverse('users:verification', args=[verification_code])
            send_mail(
                subject='Регистрация на VaGon 2.0',
                message=f'Для регистрации на платформе VaGon 2.0 пройдите по ссылке {"http://127.0.0.1:8000" + url}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.object.email]
            )
        return super().form_valid(form)


# здесь нет никакой страницы, просто выполняется верификация в бэке,
# а человека редиректит в 'users:login'
# но тоже бы хорошо всплывающее окно, мол все оки "заходите-проходите"
def user_verify(request, verification_code):
    user = User.objects.get(verification_code=verification_code)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileView(UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:profile') # уведомление всплывающее

    def get_object(self, queryset=None):
        return self.request.user


def update_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        DB_user = User.objects.get(email=email)
        new_password = secrets.token_urlsafe(nbytes=8)
        DB_user.set_password(new_password)
        DB_user.save()
        send_mail(
            subject='Смена пароля на платформе VaGon 2.0',
            message=f'Ваш новый пароль {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[DB_user.email]
        )
        return redirect(reverse_lazy('users:login'))
    return render(request, 'users/update_password.html')
