# Create your models here.
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    kyc_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"{self.username} - {self.created_at}"
    
class BvnRecords(models.Model):
    
    success = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField()
    attempted_at = models.DateTimeField(auto_now_add=True)


    
    
class Roles(models.Model):
    
    
    class RoleStatus(models.TextChoices):
        DEV = 'Dev',
        USER = 'User',
        ACCOUNTANT = 'Accountant',
        
        
    class FeatureStatus(models.TextChoices):
        VIEW_DASHBOARD = 'CanViewDashboard', 'Can View Dashboard'
        EDIT_TICKETS = 'CanEditTickets', 'Can Edit Tickets'
        NONE = 'None'
        
        
    roles = models.CharField(max_length=15, choices=RoleStatus.choices, default=RoleStatus.USER)
    feature = models.CharField(max_length=16, choices=FeatureStatus.choices, default=FeatureStatus.NONE)
    admin_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.admin_user.username}-{self.roles} - {self.feature}"


