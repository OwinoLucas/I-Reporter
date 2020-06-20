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
    validate_password = make_password
        

class InterventionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=InterventionRecord
        fields=('id','title','description','time_of_creation','time_last_edit','location','status')

class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)

    class Meta:
        model=Profile
        fields=('id',"profile_picture",'bio','contacts','user')

    