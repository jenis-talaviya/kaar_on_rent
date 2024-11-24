from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking,Vehicle
from .serializers import BookingsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


# Create your views here.

# @api_view(["POST"])
# def booking_add(request):
#         serializer = BookingsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



# @api_view(["POST"])
# def booking_add(request):
#     serializer = BookingsSerializer(data=request.data)
    
#     if serializer.is_valid():
#         # Extract the data
#         vehicle_id = serializer.validated_data.get('vehicle').id
#         start_date = serializer.validated_data.get('start_date')
#         end_date = serializer.validated_data.get('end_date')
        
#         # Ensure the start date is before the end date
#         if start_date >= end_date:
#             return Response(
#                 {"error": "End date must be after start date"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         # Check if the vehicle is available for the requested period
#         overlapping_bookings = Booking.objects.filter(
#             vehicle_id=vehicle_id,
#             start_date__lt=end_date,
#             end_date__gt=start_date
#         )
        
#         if overlapping_bookings.exists():
#             return Response(
#                 {"error": "Vehicle is already booked for the selected dates"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         # Check vehicle availability status
#         vehicle = Vehicle.objects.get(id=vehicle_id)
#         if not vehicle.availability:
#             return Response(
#                 {"error": "Vehicle is currently unavailable"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         # Save the booking
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# @api_view(["GET"])
# def booking_list(request):
#     booking = Booking.objects.all()
#     serializer = BookingsSerializer(booking, many=True)
#     return Response(serializer.data)



# # @api_view(["PUT"])
# # def booking_update(request):
# #     booking_entered_pk = request.headers.get("pk1")
# #     if not booking_entered_pk:
# #         return Response(
# #             {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
# #         )

# #     try:
# #         category = Booking.objects.get(pk=booking_entered_pk)
# #     except Booking.DoesNotExist:
# #         return Response(
# #             {"message": "booking does not exist"}, status=status.HTTP_404_NOT_FOUND
# #         )
        
# #     serializer = BookingsSerializer(category, data=request.data)
# #     if serializer.is_valid():
# #         serializer.save()
# #         return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
# #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(["PUT"])
# def booking_update(request):
#     booking_entered_pk = request.headers.get("pk1")
    
#     if not booking_entered_pk:
#         return Response(
#             {"error": "PK header is required"},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     try:
#         booking = Booking.objects.get(pk=booking_entered_pk)
#     except Booking.DoesNotExist:
#         return Response(
#             {"message": "Booking does not exist"},
#             status=status.HTTP_404_NOT_FOUND
#         )
    
#     serializer = BookingsSerializer(booking, data=request.data)
    
#     if serializer.is_valid():
#         # Extract the data
#         vehicle_id = serializer.validated_data.get('vehicle').id
#         start_date = serializer.validated_data.get('start_date')
#         end_date = serializer.validated_data.get('end_date')
        
#         # Ensure the start date is before the end date
#         if start_date >= end_date:
#             return Response(
#                 {"error": "End date must be after start date"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         # Check if the vehicle is available for the updated period
#         overlapping_bookings = Booking.objects.filter(
#             vehicle_id=vehicle_id,
#             start_date__lt=end_date,
#             end_date__gt=start_date
#         ).exclude(pk=booking.id)
        
#         if overlapping_bookings.exists():
#             return Response(
#                 {"error": "Vehicle is already booked for the selected dates"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         # Check vehicle availability status
#         vehicle = Vehicle.objects.get(id=vehicle_id)
#         if not vehicle.availability:
#             return Response(
#                 {"error": "Vehicle is currently unavailable"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         # Save the updated booking
#         serializer.save()
#         return Response({"message": "Booking updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# @api_view(["DELETE"])
# def booking_delete(request):
#     booking_entered_pk = request.headers.get("pk1")
#     if not booking_entered_pk:
#         return Response(
#             {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
#         )

#     try:
#         booking = Booking.objects.get(pk=booking_entered_pk)
#     except Booking.DoesNotExist:
#         return Response(
#             {"message": "booking does not exist"}, status=status.HTTP_404_NOT_FOUND
#         )
#     booking.delete()
#     return Response({"message": "booking deleted successfully"})



def check_role(user, allowed_roles):
    if user.role not in allowed_roles:
        return False
    return True

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def booking_add(request):
    if not check_role(request.user, ['customer']):
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = BookingsSerializer(data=request.data)
    
    if serializer.is_valid():
        # Extract the data
        vehicle_id = serializer.validated_data.get('vehicle').id
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')
        
        # Ensure the start date is before the end date
        if start_date >= end_date:
            return Response(
                {"error": "End date must be after start date"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the vehicle is available for the requested period
        overlapping_bookings = Booking.objects.filter(
            vehicle_id=vehicle_id,
            start_date__lt=end_date,
            end_date__gt=start_date
        )
        
        if overlapping_bookings.exists():
            return Response(
                {"error": "Vehicle is already booked for the selected dates"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check vehicle availability status
        vehicle = Vehicle.objects.get(id=vehicle_id)
        if not vehicle.availability:
            return Response(
                {"error": "Vehicle is currently unavailable"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save the booking
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def booking_list(request):
    if not check_role(request.user, ['admin']):
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

    bookings = Booking.objects.all()
    serializer = BookingsSerializer(bookings, many=True)
    return Response(serializer.data)



@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def booking_update(request):
    if not check_role(request.user, ['admin', 'customer']):
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
    booking_entered_pk = request.headers.get("pk1")
    
    if not booking_entered_pk:
        return Response(
            {"error": "PK header is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        booking = Booking.objects.get(pk=booking_entered_pk)
    except Booking.DoesNotExist:
        return Response(
            {"message": "Booking does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if the user is allowed to update this booking
    if request.user.role == 'customer' and booking.user != request.user:
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = BookingsSerializer(booking, data=request.data)
    
    if serializer.is_valid():
        # Extract the data
        vehicle_id = serializer.validated_data.get('vehicle').id
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')
        
        # Ensure the start date is before the end date
        if start_date >= end_date:
            return Response(
                {"error": "End date must be after start date"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the vehicle is available for the updated period
        overlapping_bookings = Booking.objects.filter(
            vehicle_id=vehicle_id,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exclude(pk=booking.id)
        
        if overlapping_bookings.exists():
            return Response(
                {"error": "Vehicle is already booked for the selected dates"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check vehicle availability status
        vehicle = Vehicle.objects.get(id=vehicle_id)
        if not vehicle.availability:
            return Response(
                {"error": "Vehicle is currently unavailable"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save the updated booking
        serializer.save()
        return Response({"message": "Booking updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def booking_delete(request):
    if not check_role(request.user, ['admin']):
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

    booking_entered_pk = request.headers.get("pk1")
    if not booking_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        booking = Booking.objects.get(pk=booking_entered_pk)
    except Booking.DoesNotExist:
        return Response(
            {"message": "Booking does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    booking.delete()
    return Response({"message": "Booking deleted successfully"})