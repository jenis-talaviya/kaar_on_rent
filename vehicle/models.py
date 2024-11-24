from django.db import models
import uuid
# Create your models here.

class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    category = models.CharField(max_length=50, choices=[('sedan', 'Sedan'), ('suv', 'SUV'), ('luxury', 'Luxury')])
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"