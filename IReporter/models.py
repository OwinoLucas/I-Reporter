from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Flag(models.Model):
    name = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default='')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default='')
    tags=models.ManyToManyField()