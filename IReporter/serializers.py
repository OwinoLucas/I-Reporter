from rest_framework import serializers,status
from IReporter.models import Profile,User,InterventionRecord
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
 
    date_joined = serializers.ReadOnlyField()
 
    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
        

class InterventionSerializer(serializers.ModelSerializer):
    # user=serializers.ReadOnlyField()
    class Meta:
        model=InterventionRecord
        fields=('id','title','description','time_of_creation',
        'time_last_edit','location','status','image','videos','user')

class ProfileSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model=Profile
        fields=('id',"profile_picture",'bio','contacts','user')

    