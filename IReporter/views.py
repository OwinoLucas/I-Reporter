from rest_framework.response import Response
from rest_framework import status
from .models import InterventionRecord
from .serializers import InterventionSerializer
from rest_framework.decorators import APIView

# pytest.ini

# Create your views here.
class InterventionList(APIView):
    def get(self,request,title):
        # GET LIST OF INTERVENTION RECORDS,POST A NEW INTERVENTION,DELETE ALL INTERVENTIONS...

        interventions = InterventionRecord.objects.filter(title__icontains=title)
        if interventions.exists():
            interventions_serializer = InterventionSerializer(interventions, many=True)
            return Response(interventions_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail':'this title was not found.'}, status=status.HTTP_404_NOT_FOUND)

class CreateIntervention(APIView):
    def post(self,request):        
        intervention_serializer = InterventionSerializer(data=request.data)
        if intervention_serializer.is_valid():
            intervention_serializer.save()
            return Response(intervention_serializer.data, status=status.HTTP_201_CREATED)
        return Response(intervention_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InterventionDetail(APIView):
    def get(self,request,pk):
    #FIND TUTORIAL BY pk(id)

        try:
            intervention=InterventionRecord.objects.get(id=pk)
        
            intervention_serializer=InterventionSerializer(intervention)
            return Response(intervention_serializer.data, status= status.HTTP_200_OK)
        except InterventionRecord.DoesNotExist:
            return Response({'detail': 'The Intervention Record does not exist.'}, status=status.HTTP_404_NOT_FOUND) 
        
    def put(self,request,pk):
        try:
            intervention=InterventionRecord.objects.get(id=pk)
            intervention_serializer=InterventionSerializer(intervention,data=request.data)
            if intervention_serializer.is_valid():
                intervention_serializer.save()
                return Response(intervention_serializer.data, status=status.HTTP_200_OK)
            return Response(intervention_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except InterventionRecord.DoesNotExist:
            return Response({'detail': 'The Intervention Record does not exist.'}, status=status.HTTP_404_NOT_FOUND) 

    def delete(self,request,pk):
        # DELETE A CERTAIN INTERVENTION RECORD
        try:
            intervention=InterventionRecord.objects.get(id=pk)
            intervention.delete()
            return Response({'detail': 'Intervention Record was deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except InterventionRecord.DoesNotExist:
            return Response({'detail': 'The Intervention Record does not exist.'}, status=status.HTTP_404_NOT_FOUND) 



class InterventionListStatus(APIView):
    def get(self,request,intervention_status):
        # Get all record items using the ntervention_status
        interventions = InterventionRecord.objects.filter(status = intervention_status)
        if interventions.exists():
            interventions_serializer = InterventionSerializer(interventions, many=True)
            return Response(interventions_serializer.data, status=status.HTTP_200_OK)
        return Response({'detail' : 'The status was not found.'}, status=status.HTTP_404_NOT_FOUND)
        


