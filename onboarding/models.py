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
    
    class bank(models.Model):
      name=models.CharField(max_length=100)
      slug=models.SlugField(max_length=100, unique=True)

    class card(models.Model):
        name = models.CharField(max_length=100)
        bank = models.ForeignKey('bank', on_delete=models.CASCADE)
        card_number = models.CharField(max_length=16, unique=True)
        expiry_date = models.DateField()
        cvv = models.CharField(max_length=3)

        def __str__(self):
            return self.name
    
    class Transaction(models.Model):
        user = models.ForeignKey(Customeruser, on_delete=models.CASCADE)
        card = models.ForeignKey('card', on_delete=models.CASCADE)
        bank = models.ForeignKey('bank', on_delete=models.CASCADE)
        amount = models.DecimalField(max_digits=10, decimal_places=2)
        transaction_date = models.DateTimeField(auto_now_add=True)
        status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')])

        def __str__(self):
            return f"Transaction {self.id} by {self.user.email} - {self.status}"
        
