from django.db import models
import uuid
import uuid
from django.contrib.auth.hashers import make_password
from django.utils import timezone

# Create your models here.

class User(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    u_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128,default=make_password('temporarypassword'))
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('customer', 'Customer')], default='customer')
    gender = models.CharField(max_length=25)
    phone_no = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    
    def __str__(self):
        return self.u_name
    
    def save(self, *args, **kwargs):
        # Hash the password with bcrypt before saving
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)


#---------------------------blacklisttoken--------------------------------------
class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token



#---------------------------------OTP-------------------------------------------
class Otp(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    expiry_time = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.email)