from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vehicle
from .serializers import VehiclesSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


# Create your views here.

# @api_view(["POST"])
# def vehicle_add(request):
#         serializer = VehiclesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def vehicle_add(request):
    if request.user.role != "admin":
        return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    serializer = VehiclesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def vehicle_list(request):
    vehicle = Vehicle.objects.all()
    serializer = VehiclesSerializer(vehicle, many=True)
    return Response(serializer.data)



# @api_view(["PUT"])
# def vehicle_update(request):
#     vehicle_entered_pk = request.headers.get("pk1")
#     if not vehicle_entered_pk:
#         return Response(
#             {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
#         )

#     try:
#         vehicle = Vehicle.objects.get(pk=vehicle_entered_pk)
#     except Vehicle.DoesNotExist:
#         return Response(
#             {"message": "vehicle does not exist"}, status=status.HTTP_404_NOT_FOUND
#         )
        
#     serializer = VehiclesSerializer(vehicle, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def vehicle_update(request):
    if request.user.role != "admin":
        return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    vehicle_entered_pk = request.headers.get("pk1")
    if not vehicle_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        vehicle = Vehicle.objects.get(pk=vehicle_entered_pk)
    except Vehicle.DoesNotExist:
        return Response(
            {"message": "Vehicle does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = VehiclesSerializer(vehicle, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Detail updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(["DELETE"])
# def vehicle_delete(request):
#     vehicle_entered_pk = request.headers.get("pk1")
#     if not vehicle_entered_pk:
#         return Response(
#             {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
#         )

#     try:
#         vehicle = Vehicle.objects.get(pk=vehicle_entered_pk)
#     except Vehicle.DoesNotExist:
#         return Response(
#             {"message": "vehicle does not exist"}, status=status.HTTP_404_NOT_FOUND
#         )
#     vehicle.delete()
#     return Response({"message": "vehicle deleted successfully"})
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def vehicle_delete(request):
    if request.user.role != 'admin':
        return Response({"error": "You do not have permission to delete vehicles."}, status=status.HTTP_403_FORBIDDEN)

    vehicle_entered_pk = request.headers.get("pk1")
    if not vehicle_entered_pk:
        return Response({"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        vehicle = Vehicle.objects.get(pk=vehicle_entered_pk)
    except Vehicle.DoesNotExist:
        return Response({"message": "Vehicle does not exist"}, status=status.HTTP_404_NOT_FOUND)

    vehicle.delete()
    return Response({"message": "Vehicle deleted successfully"})
