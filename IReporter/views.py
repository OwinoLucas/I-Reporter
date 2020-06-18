from django.shortcuts import render


from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from .models import InterventionRecord
from .serializers import InterventionSerializer
from rest_framework.decorators import api_view,APIView,permission_classes


# Create your views here.
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
    def put(self,request):        
        intervention_data = JSONParser().parse(request)
        intervention_serializer = InterventionSerializer(data=intervention_data)
        if intervention_serializer.is_valid():
            intervention_serializer.save()
            return JsonResponse(intervention_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(intervention_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def intervention_detail(request,pk):
    #FIND TUTORIAL BY pk(id)

    try:
        intervention=InterventionRecord.objects.get(id=pk)
        # GET A CERTAIN INTERVENTION
        if  request.method=='GET':
            intervention_serializer=InterventionSerializer(intervention)
            return JsonResponse(intervention_serializer.data)

        # UPDATE A CERTAIN INTERVENTION TUTORIAL
        elif request.method=='PUT':
            intervention_data=JSONParser().parse(request)
            intervention_serializer=InterventionSerializer(intervention,data=intervention_data)
            if intervention_serializer.is_valid():
                intervention_serializer.save()
                return JsonResponse(intervention_serializer.data)
            return JsonResponse(intervention_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        # DELETE A CERTAIN INTERVENTION RECORD
        elif request.method=='DELETE':
            intervention.delete()
            return JsonResponse({'message': 'Intervention Record was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except InterventionRecord.DoesNotExist:
        return JsonResponse({'message': 'The Intervention Record does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    #### GET /PUT /DELETE tutorial


@api_view(['GET',])
def intervention_list_resolved(request):
    #Get all  resolved INtervention
    intervention=InterventionRecord.objects.filter(status='resolved')

    if request.method=='GET':
        intervention_serializer=InterventionSerializer(intervention,many=True)
        return  JsonResponse(intervention_serializer.data,safe=False)




