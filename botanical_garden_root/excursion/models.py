from django.db import models
from django.contrib.auth.models import User

EXCURSION_TYPE_CHOICES = [
    ('Індивідуальні відвідування','Індивідуальні відвідування'),
    ('Екскурсія для дорослих','Екскурсія для дорослих'),
    ('Екскурсія для дітей','Екскурсія для дітей'),
    ('Проведення заходів','Проведення заходів'),
    ('Фото - відеозйомки','Фото - відеозйомки'),
]


# Create your models here.
class Excursion(models.Model):
    user = models.ForeignKey(User, blank=True, null=True ,on_delete=models.CASCADE)
    excursion_date = models.DateTimeField()
    excursion_type = models.CharField(max_length=100, choices=EXCURSION_TYPE_CHOICES)


    def __str__(self):
        return self.user.username