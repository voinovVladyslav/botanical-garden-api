from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    topic = models.CharField(max_length=50, null=True)
    message = models.CharField(max_length=1000)


    def __str__(self) -> str:
        return self.topic