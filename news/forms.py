from dataclasses import fields
from django.forms import ModelForm
from .models import News

class CreateNews(ModelForm):
    class Meta:
        model = News
        fields = '__all__'