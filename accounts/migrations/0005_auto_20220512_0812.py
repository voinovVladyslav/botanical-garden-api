# Generated by Django 3.2.12 on 2022-05-12 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20220512_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(blank=True, default='Немає', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, default='Немає', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='surname',
            field=models.CharField(blank=True, default='Немає', max_length=50, null=True),
        ),
    ]
