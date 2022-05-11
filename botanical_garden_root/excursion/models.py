from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

EXCURSION_TYPE_CHOICES = [
    ('Індивідуальні відвідування','Індивідуальні відвідування'),
    ('Екскурсія для дорослих','Екскурсія для дорослих'),
    ('Екскурсія для дітей','Екскурсія для дітей'),
    ('Проведення заходів','Проведення заходів'),
    ('Фото - відеозйомки','Фото - відеозйомки'),
]


def validate_date(value):
    if not value:
        raise ValidationError(
            _('%(value)s wrong date'),
            params={'value':value}
        )


class Excursion(models.Model):
    person = models.ForeignKey(User, blank=True, null=True ,on_delete=models.CASCADE)
    excursion_date = models.DateField(null=True, validators=[validate_date])
    excursion_time = models.TimeField(null=True)
    excursion_type = models.CharField(max_length=100, choices=EXCURSION_TYPE_CHOICES)


    def __str__(self):
        return self.person.username
