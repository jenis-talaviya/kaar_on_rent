from rest_framework import serializers

from .models import Payment

class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['booking', 'user','amount', 'payment_method', 'razorpay_order_id', 'status']
        