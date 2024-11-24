from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Payment,Booking 
from .serializers import PaymentsSerializer
from django.core.mail import send_mail
from django.conf import settings
import razorpay
import logging
from kaarrent.settings import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


# Create your views here.

logger = logging.getLogger(__name__)

def payment_page(request):
    return render(request, 'payments.html/')


# @api_view(["POST"])
# def payment_add(request):
#         serializer = PaymentsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# def payment_add(request):
#     serializer = PaymentsSerializer(data=request.data)
    
#     if serializer.is_valid():
#         # Extract booking and amount
#         booking_id = serializer.validated_data.get('booking').id
#         amount = serializer.validated_data.get('amount')
#         payment_method = serializer.validated_data.get('payment_method')  # Get the payment method from request data
        
#         # Validate booking existence
#         try:
#             booking = Booking.objects.get(id=booking_id)
#         except Booking.DoesNotExist:
#             return Response({"error": "Booking does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Validate payment amount
#         if amount != booking.total_amount:
#             return Response({"error": "Payment amount must match the total booking amount"}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Check if booking is already paid
#         if booking.status == 'paid':
#             return Response({"error": "This booking is already fully paid"}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Only proceed if the payment method is Razorpay
#         if payment_method == 'razorpay':
#             # Create a Razorpay Order
#             try:
#                 client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#                 payment_order = client.order.create({
#                     'amount': int(amount * 100),  # Razorpay expects amounts in paise
#                     'currency': 'INR',
#                     'payment_capture': '1'  # auto capture
#                 })
#             except razorpay.errors.RazorpayError as e:
#                 logger.error(f"Razorpay order creation failed: {str(e)}")
#                 return Response({"error": "Razorpay order creation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
#             # Save the payment with the Razorpay order ID
#             payment = serializer.save(
#                 razorpay_order_id=payment_order['id'],
#                 payment_method='razorpay',
#                 status='successful'  # Defaulting to 'successful' for now
#             )
            
#             # Return the Razorpay order ID to the frontend
#             return Response({
#                 "order_id": payment_order['id'],
#                 "amount": payment_order['amount'],
#                 "currency": payment_order['currency'],
#                 "razorpay_key": settings.RAZORPAY_KEY_ID
#             }, status=status.HTTP_201_CREATED)
        
#         return Response({"error": "Unsupported payment method"}, status=status.HTTP_400_BAD_REQUEST)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def payment_add(request):
    if request.user.role != 'customer':
        return Response({"error": "You do not have permission to add payments."}, status=status.HTTP_403_FORBIDDEN)

    serializer = PaymentsSerializer(data=request.data)
    if serializer.is_valid():
        # Extract booking and amount
        booking_id = serializer.validated_data.get('booking').id
        amount = serializer.validated_data.get('amount')
        payment_method = serializer.validated_data.get('payment_method')  # Get the payment method from request data
        
        # Validate booking existence
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate payment amount
        if amount != booking.total_amount:
            return Response({"error": "Payment amount must match the total booking amount"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if booking is already paid
        if booking.status == 'paid':
            return Response({"error": "This booking is already fully paid"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Only proceed if the payment method is Razorpay
        if payment_method == 'razorpay':
            # Create a Razorpay Order
            try:
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                payment_order = client.order.create({
                    'amount': int(amount * 100),  # Razorpay expects amounts in paise
                    'currency': 'INR',
                    'payment_capture': '1'  # auto capture
                })
            except razorpay.errors.RazorpayError as e:
                logger.error(f"Razorpay order creation failed: {str(e)}")
                return Response({"error": "Razorpay order creation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Save the payment with the Razorpay order ID
            payment = serializer.save(
                razorpay_order_id=payment_order['id'],
                payment_method='razorpay',
                status='successful'  # Defaulting to 'successful' for now
            )
            
            # Return the Razorpay order ID to the frontend
            return Response({
                "order_id": payment_order['id'],
                "amount": payment_order['amount'],
                "currency": payment_order['currency'],
                "razorpay_key": settings.RAZORPAY_KEY_ID
            }, status=status.HTTP_201_CREATED)
        
        return Response({"error": "Unsupported payment method"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(["POST"])
# def payment_verify(request):
#     # Extract payment details
#     razorpay_payment_id = request.data.get('razorpay_payment_id')
#     razorpay_order_id = request.data.get('razorpay_order_id')
#     razorpay_signature = request.data.get('razorpay_signature')
    
#     # Verify the payment signature
#     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#     try:
#         client.utility.verify_payment_signature({
#             'razorpay_order_id': razorpay_order_id,
#             'razorpay_payment_id': razorpay_payment_id,
#             'razorpay_signature': razorpay_signature
#         })
#     except razorpay.errors.SignatureVerificationError:
#         logger.error("Razorpay signature verification failed")
#         return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)
    
#     # Update the payment and booking status
#     try:
#         payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
#         payment.razorpay_payment_id = razorpay_payment_id
#         payment.status = 'successful'  # Mark the payment as successful
#         payment.save()
        
#         booking = payment.booking
#         booking.status = 'paid'  # Mark the booking as paid
#         booking.save()
        
#         return Response({"message": "Payment successful and verified"}, status=status.HTTP_200_OK)
#     except Payment.DoesNotExist:
#         logger.error("Payment record not found")
#         return Response({"error": "Payment record not found"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def payment_verify(request):
    if request.user.role != 'customer':
        return Response({"error": "You do not have permission to verify payments."}, status=status.HTTP_403_FORBIDDEN)

    # Extract payment details
    razorpay_payment_id = request.data.get('razorpay_payment_id')
    razorpay_order_id = request.data.get('razorpay_order_id')
    razorpay_signature = request.data.get('razorpay_signature')
    
    # Verify the payment signature
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
    except razorpay.errors.SignatureVerificationError:
        logger.error("Razorpay signature verification failed")
        return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Update the payment and booking status
    try:
        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        payment.razorpay_payment_id = razorpay_payment_id
        payment.status = 'successful'  # Mark the payment as successful
        payment.save()
        
        booking = payment.booking
        booking.status = 'paid'  # Mark the booking as paid
        booking.save()
        
        return Response({"message": "Payment successful and verified"}, status=status.HTTP_200_OK)
    except Payment.DoesNotExist:
        logger.error("Payment record not found")
        return Response({"error": "Payment record not found"}, status=status.HTTP_400_BAD_REQUEST)




# @api_view(["GET"])
# def payment_list(request):
#     payment = Payment.objects.all()
#     serializer = PaymentsSerializer(payment, many=True)
#     return Response(serializer.data)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def payment_list(request):
    if request.user.role != 'admin':
        return Response({"error": "You do not have permission to view payments."}, status=status.HTTP_403_FORBIDDEN)

    payment = Payment.objects.all()
    serializer = PaymentsSerializer(payment, many=True)
    return Response(serializer.data)



# @api_view(["PUT"])
# def payment_update(request):
#     payment_entered_pk = request.headers.get("pk1")
#     if not payment_entered_pk:
#         return Response(
#             {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
#         )

#     try:
#         payment = Payment.objects.get(pk=payment_entered_pk)
#     except Payment.DoesNotExist:
#         return Response(
#             {"message": "payment does not exist"}, status=status.HTTP_404_NOT_FOUND
#         )
        
#     serializer = PaymentsSerializer(payment, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def payment_update(request):
    if request.user.role != 'admin':
        return Response({"error": "You do not have permission to update payments."}, status=status.HTTP_403_FORBIDDEN)

    payment_entered_pk = request.headers.get("pk1")
    if not payment_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        payment = Payment.objects.get(pk=payment_entered_pk)
    except Payment.DoesNotExist:
        return Response(
            {"message": "Payment does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = PaymentsSerializer(payment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Payment updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(["DELETE"])
# def payment_delete(request):
#     payment_entered_pk = request.headers.get("pk1")
#     if not payment_entered_pk:
#         return Response(
#             {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
#         )

#     try:
#         payment = Payment.objects.get(pk=payment_entered_pk)
#     except Payment.DoesNotExist:
#         return Response(
#             {"message": "payment does not exist"}, status=status.HTTP_404_NOT_FOUND
#         )
#     payment.delete()
#     return Response({"message": "payment deleted successfully"})
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def payment_delete(request):
    if request.user.role != 'admin':
        return Response({"error": "You do not have permission to delete payments."}, status=status.HTTP_403_FORBIDDEN)

    payment_entered_pk = request.headers.get("pk1")
    if not payment_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        payment = Payment.objects.get(pk=payment_entered_pk)
    except Payment.DoesNotExist:
        return Response(
            {"message": "Payment does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    payment.delete()
    return Response({"message": "Payment deleted successfully"})