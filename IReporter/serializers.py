from rest_framework import serializers 
from.models import User,InterventionRecord
from django.contrib.auth.hashers import make_password
 
 
class UserSerializer(serializers.ModelSerializer):
 
    date_joined = serializers.ReadOnlyField()
 
    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password')
        #extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class UserRegSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate_email(self, email):
        existing = User.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError("Someone with that email "
                "address has already registered. Was it you?")

        return email

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and "
                "confirm it.")

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
          
        return data
 

class InterventionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=InterventionRecord
        fields=('id','title','description','time_of_creation','time_last_edit','location','status')

 
   #     password = validate_data["password"]
    #     confirm_password = validate_data["confirm_password"]
    #     if password != confirm_password:
    #         raise serializers.ValidationError(
    #     {"password":"confirm password must match password."})
    #     user = User(email=email, **extra_fields)
    #     user.set_password(password)
    #     # validate_password = make_password
    #     user.save()
    #     return user
        