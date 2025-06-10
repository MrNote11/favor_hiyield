import random
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser

class Customeruser(AbstractUser):
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    is_admin = models.BooleanField(default=False)  

    def __str__(self):
        return self.username or self.email

class OTP(models.Model):
    user = models.ForeignKey(Customeruser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.email}: {self.otp}"
    
    def generate_otp(self):
<<<<<<< HEAD
        self.otp = str(random.randint(100000, 999999))
        self.created_at = timezone.now()
=======
        self.otp = str(random.randint(100000, 999999))  # Generates a 6-digit OTP
        self.created_at = timezone.now()  
>>>>>>> 9ecc41afb69907099cb3581d65be9e9d18914bdc
        self.save()
        return self.otp

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)
