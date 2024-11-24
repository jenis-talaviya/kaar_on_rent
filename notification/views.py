from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationsSerializer

# Create your views here.

@api_view(["POST"])
def notification_add(request):
        serializer = NotificationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def notification_list(request):
    notification = Notification.objects.all()
    serializer = NotificationsSerializer(notification, many=True)
    return Response(serializer.data)



@api_view(["PUT"])
def notification_update(request):
    notification_entered_pk = request.headers.get("pk1")
    if not notification_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        notification = Notification.objects.get(pk=notification_entered_pk)
    except Notification.DoesNotExist:
        return Response(
            {"message": "notification does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = NotificationsSerializer(notification, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
def notification_delete(request):
    notification_entered_pk = request.headers.get("pk1")
    if not notification_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        notification = Notification.objects.get(pk=notification_entered_pk)
    except Notification.DoesNotExist:
        return Response(
            {"message": "notification does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    notification.delete()
    return Response({"message": "notification deleted successfully"})
