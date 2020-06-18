from django.shortcuts import render
from IReporter.models import Profile
from IReporter.serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class ProfileList(APIView):
    '''
    class to define view for the profile api endpoint
    '''
    def get(self, request, format=None):
        all_profiles=Profile.objects.all()
        serializers=ProfileSerializer(all_profiles,many=True)
        return Response(serializers.data)
    def post():


