from rest_framework import serializers
from IReporter.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Profile
        fields=('id',"profile_picture",'bio','contacts')