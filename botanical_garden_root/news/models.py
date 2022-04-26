from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=100)
    news = models.TextField()
    preview = models.ImageField(null=True, blank=True)
    publication_date = models.DateTimeField('Last Updated')
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
