from rest_framework import serializers
from.models import User
 
 
class UserSerializer(serializers.ModelSerializer):
 
    date_joined = serializers.ReadOnlyField()
 
    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}

# class LoginSerializer(serializers.ModelSerializer):
    
#     class Meta(object):
#         model = User
#         fields = ( 'email','password')
#         extra_kwargs = {'password': {'write_only': True}}