# Generated by Django 3.2.15 on 2022-09-02 14:32

from django.db import migrations, models
import news.models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.ImageField(null=True, upload_to=news.models.news_image_file_path),
        ),
    ]