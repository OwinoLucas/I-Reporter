# Generated by Django 3.0.7 on 2020-06-19 12:26

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IReporter', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='interventionrecord',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='image'),
        ),
        migrations.AddField(
            model_name='interventionrecord',
            name='video',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='video'),
        ),
    ]
