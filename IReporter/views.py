from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.settings import api_settings
from .serializers import UserSerializer,InterventionSerializer,UserRegSerializer
from .models import User,InterventionRecord
import jwt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework.decorators import api_view,APIView,permission_classes

# Create your views here.

class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,) 
    def post(self, request):
        # Validating our serializer from the UserRegSerializer
        serializer = UserRegSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Everything's valid, so send it to the UserSerializer
        model_serializer = UserSerializer(data=serializer.data)
        model_serializer.is_valid(raise_exception=True)
        model_serializer.save()
        return Response(model_serializer.data, status=status.HTTP_201_CREATED)
        
class LoginApiView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']          
            user = User.objects.get(email=email, password=password)          
            if user:
                try:
                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    #import pdb; pdb.set_trace()
                    user_details = {}
                    user_details['name'] = "%s %s" % (
                        user.first_name, user.last_name)
                    user_details['token'] = token
                    # user_logged_in.send(sender=user.__class__,
                    #                     request=request, user=user)               
                    return Response({'msg': 'Login successful', 'user_details':user_details }, status=status.HTTP_200_OK)

                except:
                    return Response({'msg': 'Account not approved or wrong Password.'}, status=status.HTTP_409_CONFLICT)
            else:           
                return Response({'msg': 'Can not authenticate with the given credentials or the account has been deactivated'}, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            return Response({'msg': 'please provide a email and a password'}, status=status.HTTP_401_UNAUTHORIZED)

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





