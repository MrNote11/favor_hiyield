import random
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser

class Customeruser(AbstractUser):
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    blacklist = models.BooleanField(default=False)

    def __str__(self):
        return self.username or self.email

class OTP(models.Model):
    user = models.ForeignKey(Customeruser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.email}: {self.otp}"

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.created_at = timezone.now()
        self.save()
        return self.otp

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)
