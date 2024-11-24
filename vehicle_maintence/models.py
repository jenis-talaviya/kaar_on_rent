from django.db import models
import uuid
from vehicle.models import Vehicle
# Create your models here.

class VehicleMaintenance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_records')
    service_date = models.DateTimeField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    next_service_due = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
