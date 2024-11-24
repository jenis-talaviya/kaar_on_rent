from django.db import models
import uuid
from users.models import User
# Create your models here.

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[('booking_reminder', 'Booking Reminder'), ('payment_confirmation', 'Payment Confirmation')])
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
