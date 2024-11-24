from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VehicleMaintenance
from .serializers import VehiclemaintencesSerializer

# Create your views here.

@api_view(["POST"])
def vehiclemaintaine_add(request):
        serializer = VehiclemaintencesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def vehiclemaintaine_list(request):
    vehiclemaintaine = VehicleMaintenance.objects.all()
    serializer = VehiclemaintencesSerializer(vehiclemaintaine, many=True)
    return Response(serializer.data)



@api_view(["PUT"])
def vehiclemaintaine_update(request):
    vehiclemaintaine_entered_pk = request.headers.get("pk1")
    if not vehiclemaintaine_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        vehiclemaintaine = VehicleMaintenance.objects.get(pk=vehiclemaintaine_entered_pk)
    except VehicleMaintenance.DoesNotExist:
        return Response(
            {"message": "vehiclemaintaine does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = VehicleMaintenance(vehiclemaintaine, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
def vehiclemaintaine_delete(request):
    vehiclemaintaine_entered_pk = request.headers.get("pk1")
    if not vehiclemaintaine_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        vehiclemaintaine = VehicleMaintenance.objects.get(pk=vehiclemaintaine_entered_pk)
    except VehicleMaintenance.DoesNotExist:
        return Response(
            {"message": "vehiclemaintaine does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    vehiclemaintaine.delete()
    return Response({"message": "vehiclemaintaine deleted successfully"})
