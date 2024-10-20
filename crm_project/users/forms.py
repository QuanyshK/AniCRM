from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','bio', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio']


class ManagerAccessForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_manager']


