from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.settings import api_settings
from .serializers import UserSerializer
from .models import User
import jwt
from .email import send_welcome_email
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import UserSerializer
# from django.core.mail import EmailMessage
# Create your views here.

class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,)
    # def send_email():
    # email = EmailMessage(
    #     'Title',
    #     (UserSerializer.first_name, UserSerializer.email, ),
    #     'my-email',
    #     ['my-receive-email']
    # )
    # email.attach_file(ConsultSerializer.file)
    # email.send()
 
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
            # send_welcome_email(first_name,email)
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
