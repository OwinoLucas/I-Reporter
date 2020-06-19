from rest_framework import serializers
from.models import User
from django.contrib.auth.hashers import make_password
 
class UserSerializer(serializers.ModelSerializer):
 
    date_joined = serializers.ReadOnlyField()
 
    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    validate_password = make_password
        

# class SubscribersSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Subscribers
#         fields = ( 'name', 'email')
       