from django.db import models
from django.conf import settings

import uuid
import os


def news_image_file_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'news', filename)


class News(models.Model):
    title = models.CharField(max_length=255)
    context = models.TextField()
    hashtag = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publication_date = models.DateField(auto_now_add=True)
    image = models.ImageField(null=True, upload_to=news_image_file_path)

    def __str__(self):
        return self.title
