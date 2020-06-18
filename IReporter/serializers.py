from rest_framework import serializers
from .models import InterventionRecord


class InterventionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=InterventionRecord
        fields=('id','title','description','time_of_creation','time_last_edit','location','status')