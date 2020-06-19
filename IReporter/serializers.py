from rest_framework import serializers
from .models import Flag,Tag


class FlagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Flag
        fields = '__all__'
        
class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Tag
        fields='__all__'      