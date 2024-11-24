from rest_framework import serializers

from .models import Vehicle

class VehiclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
        