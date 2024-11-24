from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Invoice,Booking
from .serializers import InvoiceSerializer
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

# @api_view(["POST"])
# def invoice_add(request):
#         serializer = InvoiceSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def invoice_add(request):
    serializer = InvoiceSerializer(data=request.data)
    
    if serializer.is_valid():
        # Extract the data
        booking_id = serializer.validated_data.get('booking').id
        
        # Ensure the booking exists
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Prevent duplicate invoices for the same booking
        if Invoice.objects.filter(booking=booking).exists():
            return Response(
                {"error": "An invoice already exists for this booking"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save the invoice
        invoice = serializer.save()

        # Send invoice details via email
        user_email = booking.user.email
        vehicle = booking.vehicle
        send_mail(
            subject="Your Invoice Details",
            message=f"Dear {booking.user.u_name},\n\n"
                    f"Your invoice has been generated for the booking.\n"
                    f"Booking Details:\n"
                    f"Vehicle: {vehicle.make} {vehicle.model}\n"
                    f"Invoice Amount: {Invoice.amount}\n"
                    f"Due Date: {Invoice.due_date}\n\n"
                    f"Thank you for using our service!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def invoice_list(request):
    invoice = Invoice.objects.all()
    serializer = InvoiceSerializer(invoice, many=True)
    return Response(serializer.data)



@api_view(["PUT"])
def invoice_update(request):
    invoice_entered_pk = request.headers.get("pk1")
    if not invoice_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        invoice = Invoice.objects.get(pk=invoice_entered_pk)
    except Invoice.DoesNotExist:
        return Response(
            {"message": "invoice does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = InvoiceSerializer(invoice, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
def invoice_delete(request):
    invoice_entered_pk = request.headers.get("pk1")
    if not invoice_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        invoice = Invoice.objects.get(pk=invoice_entered_pk)
    except Invoice.DoesNotExist:
        return Response(
            {"message": "invoice does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    invoice.delete()
    return Response({"message": "invoice deleted successfully"})
