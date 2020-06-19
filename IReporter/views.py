from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .models import Flag
from .serializers import FlagSerializer,TagSerializer
from rest_framework.decorators import api_view,APIView,permission_classes


# Create your views here.
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




