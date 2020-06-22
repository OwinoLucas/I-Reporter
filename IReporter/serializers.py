from rest_framework import serializers 
from .models import InterventionRecord
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, 
        validators=[UniqueValidator(queryset=User.object.all())]) 
    username = serializers.CharField(
        max_length = 32, 
        validators=[UniqueValidator(queryset=User.object.all())])
    first_name = serializers.CharField(
        max_length = 32)
    last_name = serializers.CharField(
        max_length = 32)
    password = serializers.CharField(
        min_length = 5,
        write_only = True)
        
    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
          )
        return user

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password')
    

class InterventionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=InterventionRecord
        fields=('id','title','description','time_of_creation','time_last_edit','location','status')

