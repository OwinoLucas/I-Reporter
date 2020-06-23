from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import InterventionSerializer,UserSerializer
from .models import InterventionRecord 
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.

class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,) 
    def post(self, request):
        # Validating our serializer from the UserSerializer
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            subject = 'welcome'
            body = '''
                    Greetings from the I-reporter Team,
                    Hello ''' + user_serializer.data['username'] + ''', we are glad having you as one of our
                    entrusted clients to give news and update the different agencies on the country's development.
                    
                    We ensure that your voices will be heard!
                    Cheers, 
                    The I-reporter team. '''
            sender = settings.EMAIL_HOST_USER
            receiver = user_serializer.data['email']
            
            send_mail(subject,body,sender,[receiver])
            return Response({'detail' : 'User successfully created.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        
class LoginApiView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        user = authenticate(request, 
                          username=request.data['username'],
                          password=request.data['password'])
        if user is not None:
            try:
                user_token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                user_token = Token.objects.create(user=user)
            return Response({'token' : user_token.key}, status = status.HTTP_201_CREATED)
        else:
            return Response({'detail' : 'username or password is incorrect.'}, status= status.HTTP_400_BAD_REQUEST)

class intervention_list(APIView):
    def get(self,request):
    #GET LIST OF INTERVENTION RECORDS,POST A NEW INTERVENTION,DELETE ALL INTERVENTIONS...
        intervention =InterventionRecord.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            intervention = InterventionRecord.filter(title__icontains=title)
        
        intervention_serializers = InterventionSerializer(intervention, many=True)
        return JsonResponse(intervention_serializers.data, safe=False)

    # #CREATE AND SAVE A NEW INTERVENTION RECORD
    def post(self,request):        
        intervention_data = JSONParser().parse(request)
        intervention_serializer = InterventionSerializer(data=intervention_data)
        if intervention_serializer.is_valid():
            intervention_serializer.save()
            return JsonResponse(intervention_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(intervention_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class intervention_detail(APIView):
    def get(self,request,pk):
    #FIND TUTORIAL BY pk(id)

        try:
            intervention=InterventionRecord.objects.get(id=pk)
        
            intervention_serializer=InterventionSerializer(intervention)
            return JsonResponse(intervention_serializer.data)
        except InterventionRecord.DoesNotExist:
            return JsonResponse({'message': 'The Intervention Record does not exist!'}, status=status.HTTP_404_NOT_FOUND) 
        
    def put(self,request,pk):
        try:
            intervention=InterventionRecord.objects.get(id=pk)
            intervention_data=JSONParser().parse(request)
            intervention_serializer=InterventionSerializer(intervention,data=intervention_data)
            if intervention_serializer.is_valid():
                intervention_serializer.save()
                return JsonResponse(intervention_serializer.data)
            return JsonResponse(intervention_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except InterventionRecord.DoesNotExist:
            return JsonResponse({'message': 'The Intervention Record does not exist!'}, status=status.HTTP_404_NOT_FOUND) 
    def delete(self,request,pk):
        # DELETE A CERTAIN INTERVENTION RECORD
        
        try:
            intervention=InterventionRecord.objects.get(id=pk)
            intervention.delete()
            return JsonResponse({'message': 'Intervention Record was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except InterventionRecord.DoesNotExist:
            return JsonResponse({'message': 'The Intervention Record does not exist!'}, status=status.HTTP_404_NOT_FOUND) 



class intervention_list_status(APIView):
    def get(self,request):
        #Get all  resolved INtervention
        try:
            intervention=InterventionRecord.objects.filter(status='resolved')
            intervention_serializer=InterventionSerializer(intervention,many=True)
            return  JsonResponse(intervention_serializer.data,safe=False)
        except InterventionRecord.DoesNotExist:
            return JsonResponse({'message': 'The Status does not exist!'}, status=status.HTTP_404_NOT_FOUND) 





