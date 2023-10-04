from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# from catalog.forms import StyleFormMixin
from users.models import User


# class UserRegisterForm(StyleFormMixin, UserCreationForm):
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


# class UserUpdateForm(StyleFormMixin, UserChangeForm):
class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'country', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
