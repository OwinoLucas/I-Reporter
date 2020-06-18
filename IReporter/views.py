from django.shortcuts import render
from IReporter.models import Profile,User
from IReporter.serializers import ProfileSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.parsers import MultiPartParser,JSONParser,FileUploadParser
import cloudinary.uploader
from django.http.response import JsonResponse
import jwt
from rest_framework_jwt.settings import api_settings
# Create your views here.
class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,)
 
    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class LoginApiView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']

            user = User.objects.get(email=email, password=password)
            # import pdb; pdb.set_trace()
            if user:
                try:
                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
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

