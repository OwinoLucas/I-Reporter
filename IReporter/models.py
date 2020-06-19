from django.db import models

# Create your models here.

class InterventionRecord(models.Model):
    STATUS=[
        ('Under Investigation','Under Investigation'),
        ('rejected','rejected'),
        ('resolved','resolved')
    ]
    title=models.CharField(max_length=50,blank=False,default='')
    description=models.TextField()
    time_of_creation=models.DateTimeField(auto_now_add=True)
    time_last_edit=models.DateTimeField(auto_now=True)
    location=models.CharField(max_length=50,blank=True)##UP FOR REVIEW####
    status=models.CharField(max_length=250,choices=STATUS,default='')
    
