from dataclasses import field
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Customer

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class CustomerFrom(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'date_created']