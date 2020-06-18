from django.shortcuts import render
from IReporter.models import Profile
from IReporter.serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


# Create your views here.
class ProfileList(APIView):
    '''
    class to define view for the profile api endpoint
    '''
    def get(self, request, format=None):
        all_profiles=Profile.objects.all()
        serializers=ProfileSerializer(all_profiles,many=True)
        return Response(serializers.data)
        
    def post(self,request,format=None):
        serializers= ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)    

