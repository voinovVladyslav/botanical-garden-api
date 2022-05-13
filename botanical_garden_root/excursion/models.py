from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from datetime import date
from accounts.models import Customer

EXCURSION_TYPE_CHOICES = [
    ('Індивідуальні відвідування','Індивідуальні відвідування'),
    ('Екскурсія для дорослих','Екскурсія для дорослих'),
    ('Екскурсія для дітей','Екскурсія для дітей'),
    ('Проведення заходів','Проведення заходів'),
    ('Фото - відеозйомки','Фото - відеозйомки'),
]

def validate_date(value):
    today = date.today()
    if value < today:
        raise ValidationError(
            _('Ми не працюємо в минулому'),
            params={'value':value}
        )

    if value == today:
        raise ValidationError(
            _('Неможливо записатися на сьогодні'),
            params={'value':value}
        )

    if value.weekday() in [5, 6]:
        raise ValidationError(
            _('В цей день у нас вихідний'),
            params={'value':value}
        )


def validate_time(value):
    if  value.hour < 8:
        raise ValidationError(
            _('Записатися раніше 8:30 неможливо'),
            params={'value':value}
        )

    if  value.hour >= 15 and value.minute != 0:
        raise ValidationError(
            _('Записатися пізніше 15 години неможливо'),
            params={'value':value}
        )

    if  value.hour == 8 and value.minute < 30:
        raise ValidationError(
            _('Записатися раніше 8:30 неможливо'),
            params={'value':value}
        )
    


class Excursion(models.Model):
    person = models.ForeignKey(Customer, blank=True, null=True ,on_delete=models.CASCADE)
    excursion_date = models.DateField(null=True, validators=[validate_date])
    excursion_time = models.TimeField(null=True, validators=[validate_time])
    excursion_type = models.CharField(max_length=100, choices=EXCURSION_TYPE_CHOICES)
    
    
    def __str__(self):
        return self.person.user.username
