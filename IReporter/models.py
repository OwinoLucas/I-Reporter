from django.db import models

# Create your models here.

class InterventionRecord(models.Model):
    STATUS=(
        ('Under Investigation','Under Investigation'),
        ('rejected','rejected'),
        ('resolved','resolved')
    )
    title=models.CharField(max_length=50,blank=False)
    description=models.TextField(blank=True, null=True)
    time_of_creation=models.DateTimeField(auto_now_add=True)
    time_last_edit=models.DateTimeField(auto_now=True)
    location=models.CharField(max_length=50,blank=True)
    status=models.CharField(max_length=20,choices=STATUS, blank=True, null=True)


