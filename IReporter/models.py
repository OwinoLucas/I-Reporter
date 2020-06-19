from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Tag(models.Model):
    tags = models.CharField(max_length=100)

    def __str__(self):
        return self.tags


class Flag(models.Model):
    title = models.CharField(max_length=100)
    description=models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default='')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default='')
    tags=models.ManyToManyField(Tag)
    
    class Meta:
        verbose_name_plural = "Flags"
        
        