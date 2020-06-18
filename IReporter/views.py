from django.shortcuts import render
from IReporter.models import Profile
from IReporter.serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser,JSONParser,FileUploadParser
import cloudinary.uploader
from django.http.response import JsonResponse
# Create your views here.
class ProfileList(APIView):
    '''
    class to define view for the profile api endpoint
    '''
    
    def get(self, request, format=None):
        all_profiles=Profile.objects.all()
        serializers=ProfileSerializer(all_profiles,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)    

class SingleProfile(APIView):
    '''
    class to define view for returning one profile
    '''
    def get(self,request,pk):
        try:
            profile=Profile.objects.get(pk=pk)
            profile_serializer=ProfileSerializer(profile)
            return Response(profile_serializer.data)
        except Profile.DoesNotExist:
            return JsonResponse({'Message':"object does not exist"}, status=status.HTTP_404_NOT_FOUND)    
             
    def put(self,request,pk):
        parser_classes=[JSONParser,FileUploadParser,MultiPartParser]
        try:
            profile=Profile.objects.get(pk=pk)
            profile_serializer=ProfileSerializer(profile,data=request.data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response(profile_serializer.data)
            return Response(profile_serializer.errors,status=status.HTTP_400_BAD_REQUEST)    
        except Profile.DoesNotExist:
            return JsonResponse({'Message':"object does not exist"}, status=status.HTTP_404_NOT_FOUND) 