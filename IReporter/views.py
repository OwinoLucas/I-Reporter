from rest_framework.response import Response
from rest_framework import status
from .models import InterventionRecord,Flag
from .serializers import InterventionSerializer,FlagSerializer,TagSerializer
from rest_framework.decorators import APIView
from django.shortcuts import render 
from IReporter.models import Profile,User,InterventionRecord
from IReporter.serializers import ProfileSerializer,UserSerializer,InterventionSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.parsers import MultiPartParser,JSONParser,FileUploadParser
import cloudinary.uploader
from django.http.response import JsonResponse
import jwt
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import api_view,APIView,permission_classes

# pytest.ini

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import UserSerializer

# Create your views here.






class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,) 
    def post(self, request):
        current_user=request.user
        user = request.data
        print(current_user)
        serializer = UserSerializer(data=user)
        
        serializer.is_valid(raise_exception=True)
        serializer.user=current_user
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
    permission_classes = (IsAuthenticated,)
 
    def get(self, request, format=None):
        all_profiles=Profile.objects.all()
        serializers=ProfileSerializer(all_profiles,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        def add_user_data(data,user):
            data['user']=user.id
            return data
        serializers = ProfileSerializer(data=add_user_data(request.data,request.user))
        
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)    

class SingleProfile(APIView):
    '''
    class to define view for returning one profile
    '''
    permission_classes = (IsAuthenticated,)
 
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
            def add_user_data(data,user):
                request.data_mutable=True
                data['user']=user.id
                return data
            profile_serializer=ProfileSerializer(profile,data=add_user_data(request.data,request.user))
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response(profile_serializer.data)
            return Response(profile_serializer.errors,status=status.HTTP_400_BAD_REQUEST)    
        except Profile.DoesNotExist:
            return JsonResponse({'Message':"object does not exist"}, status=status.HTTP_404_NOT_FOUND) 
    
    # *****GETTING ALL INTERVENTION RECORDS****

class CreateInterventionRecord(APIView):
    
    def post(self,request): 
        current_user=request.user   
        data=request.data
        data['user']=current_user.id
        intervention_serializer = InterventionSerializer(data=data)
        if intervention_serializer.is_valid():
            intervention_serializer.save()
            return Response(intervention_serializer.data, status=status.HTTP_201_CREATED)
        return Response(intervention_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class InterventionList(APIView):
    def get(self,request,title):
        # GET LIST OF INTERVENTION RECORDS,POST A NEW INTERVENTION,DELETE ALL INTERVENTIONS...

        interventions = InterventionRecord.objects.filter(title__icontains=title)
        if interventions.exists():
            interventions_serializer = InterventionSerializer(interventions, many=True)
            return Response(interventions_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail':'this title was not found.'}, status=status.HTTP_404_NOT_FOUND)
class AllInterventionRecords(APIView):
    
    def get(self,request):
    #GET LIST OF INTERVENTION RECORDS,POST A NEW INTERVENTION,DELETE ALL INTERVENTIONS...
        intervention =InterventionRecord.objects.all()
        current_user=self.request.user
        print(current_user)
        title = request.GET.get('title', None)
        if title is not None:
            intervention = InterventionRecord.filter(title__icontains=title)
        
        intervention_serializers = InterventionSerializer(intervention, many=True)
        return JsonResponse(intervention_serializers.data, safe=False)

    # #CREATE AND SAVE A NEW INTERVENTION RECORD
    def post(self,request,format=None):        
        def add_user_data(data,user):
                data['profile']=user.id
                return data
        intervention_serializer = InterventionSerializer(data=add_user_data(request.data,request.user))
        if intervention_serializer.is_valid():
            intervention_serializer.save()
            return Response(intervention_serializer.data, status=status.HTTP_201_CREATED) 
        return Response(intervention_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InterventionDetail(APIView):
    def get(self,request,pk):
    #FIND TUTORIAL BY pk(id)

        try:
            intervention=InterventionRecord.objects.get(pk=pk)
        
            intervention_serializer=InterventionSerializer(intervention)
            return Response(intervention_serializer.data, status= status.HTTP_200_OK)
        except InterventionRecord.DoesNotExist:
            return Response({'detail': 'The Intervention Record does not exist.'}, status=status.HTTP_404_NOT_FOUND) 
        
    def put (self,request,pk):
        intervention=InterventionRecord.objects.get(id=pk)  
        # tutorial_data = JSONParser().parse(request)
        def add_user_data(data,user):
            request.data_mutable=True
            data['user']=user.id
            return data
        intervention_serializer=InterventionSerializer(intervention,data=add_user_data(request.data,request.user))
        print(intervention_serializer)
        if intervention_serializer.is_valid():
            intervention_serializer.save()
            return Response(intervention_serializer.data, status=status.HTTP_200_OK)
        return Response(intervention_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
         

    def delete(self,request,pk):
        # DELETE A CERTAIN INTERVENTION RECORD
        try:
            intervention=InterventionRecord.objects.get(id=pk)
            intervention.delete()
            return Response({'detail': 'Intervention Record was deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except InterventionRecord.DoesNotExist:
            return Response({'detail': 'The Intervention Record does not exist.'}, status=status.HTTP_404_NOT_FOUND) 
          
class flag_list(APIView):
    def get(self,request):
    #list of all red flags
        flags =Flag.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            flags = Flag.filter(title__icontains=title)
        
        flag_serializers = FlagSerializer(flags, many=True)
        return JsonResponse(flag_serializers.data, safe=False)

    # function to create and save new flag instance
    def post(self,request):        
        flag_data = JSONParser().parse(request)
        flag_serializer =FlagSerializer(data=flag_data)
        if flag_serializer.is_valid():
            flag_serializer.save()
            return JsonResponse(flag_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(flag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class flag_detail(APIView):
    def get(self,request,pk):
    #funtion to find a flag by id(PK) 

        try:
            flags=Flag.objects.get(id=pk)
        
            flag_serializer=FlagSerializer(flags)
            return JsonResponse(flag_serializer.data)
        except Flag.DoesNotExist:
            return JsonResponse({'message': 'Record does not exist!'}, status=status.HTTP_404_NOT_FOUND) 
        
    def put(self,request,pk):
        try:
            flags=Flag.objects.get(id=pk)
            flag_data=JSONParser().parse(request)
            flag_serializer=FlagSerializer(flags,data=flag_data)
            if flag_serializer.is_valid():
                flag_serializer.save()
                return JsonResponse(flag_serializer.data)
            return JsonResponse(flag_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Flag.DoesNotExist:
            return JsonResponse({'message': 'Record soes not exist!'}, status=status.HTTP_404_NOT_FOUND) 
    def delete(self,request,pk):
        # function to delete a user flag object
        
        try:
            flags=Flag.objects.get(id=pk)
            flags.delete()
            return JsonResponse({'message': 'Flag Record  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except Flag.DoesNotExist:
            return JsonResponse({'message': ' Flag Record does not exist!'}, status=status.HTTP_404_NOT_FOUND)          



class InterventionListStatus(APIView):
    def get(self,request,intervention_status):
        # Get all record items using the ntervention_status
        interventions = InterventionRecord.objects.filter(status = intervention_status)
        if interventions.exists():
            interventions_serializer = InterventionSerializer(interventions, many=True)
            return Response(interventions_serializer.data, status=status.HTTP_200_OK)
        return Response({'detail' : 'The status was not found.'}, status=status.HTTP_404_NOT_FOUND)
        




