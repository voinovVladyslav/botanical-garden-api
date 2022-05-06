from django.db import models

# Create your models here.
class Contact(models.Model):
    user_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    user_email = models.EmailField()
    user_message = models.CharField(max_length=1000)
