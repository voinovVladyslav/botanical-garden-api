from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=100)
    context = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    hashtag = models.CharField(max_length=20, null=True, blank=True)


    def __str__(self):
        return self.title