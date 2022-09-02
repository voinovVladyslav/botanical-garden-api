from django.db import models
from django.conf import settings


class News(models.Model):
    title = models.CharField(max_length=255)
    context = models.TextField()
    hashtag = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publication_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
