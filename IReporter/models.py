from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.
class Profile(models.Model):
    '''
    profile class to define profile objects
    '''
    profile_picture=CloudinaryField('picture',blank=True)
    bio=models.CharField(max_length=100,blank=True)
    contacts=models.CharField(max_length=30,blank=True)


