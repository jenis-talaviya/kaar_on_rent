from rest_framework import serializers

from .models import VehicleMaintenance

class VehiclemaintencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleMaintenance
        fields = "__all__"
        