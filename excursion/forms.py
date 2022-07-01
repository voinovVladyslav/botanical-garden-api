from django.forms import ModelForm
from django import forms
from .models import Excursion

class ExcursionForm(ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}))
    time = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'time'}))
    class Meta:
        model = Excursion
        fields = '__all__'