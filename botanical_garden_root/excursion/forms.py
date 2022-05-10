from django.forms import ModelForm
from .models import Excursion

class ExcursioinFrom(ModelForm):
    class Meta:
        model = Excursion
        fields = '__all__'