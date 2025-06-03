from rest_framework import serializers
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404 
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password 
from django.contrib.auth.models import User
import re
import secrets
from django.core.mail import send_mail
from django.conf import settings
from models import Roles, Features

class SignUpAdminSerializers(serializers.ModelSerializer):
    
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    class Meta:
        model = User
        fields = ['firsname', 'lastname', 'email', 'username']
       
    def create(self, data):
        password = secrets.token_urlsafe(10)  # Generate random password
        username = data.get("username")
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        user = User.objects.create_superuser(
            username=username,first_name=first_name, 
            last_name=last_name,
            email=email, password=password, 
        )
        

        # Send password via email
        send_mail(
            subject='Your Super Admin Credentials',
            message=f'Your password: {password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
            
        
        )
        return user
    
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
    
class AssignRolesAndFeatures(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = ['roles', 'user', 'features']