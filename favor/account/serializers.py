from datetime import timedelta
from rest_framework import serializers
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404 
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password 
from django.contrib.auth.models import User
import re
from django.utils import timezone
import secrets
from django.core.mail import send_mail
from django.conf import settings
from .models import Roles, CustomUser, BvnRecords
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import OTP
import os
from dotenv import load_dotenv
import random
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
load_dotenv()



class AdminLoginSerialisers(serializers.ModelSerializer):
    phone_no = serializers.CharField(max_length=15, required=False, allow_blank=True)
    class Meta:
        model = User
        fields = ('email', 'password','phone_no')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate(self, data):
        email= data.get('email')
        phone_no = data.get('phone_no')
        if not email and not phone_no:
            raise serializers.ValidationError("Email or Phone number is required")
        
        user=None
        if email:
            try:
                user=User.objects.filter(email=email).first()
            except:
                raise serializers.ValidationError("Invalid email format")
        elif phone_no:
            try:
                user=User.objects.filter(profile__phone_no=phone_no).first()
            except:
                raise serializers.ValidationError("Incorrect Phone Number")

        return data


User = get_user_model()

class AdminForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User with this email does not exist.")
        self.user = user
        return email

    def create(self, validated_data):
        otp_obj, _ = OTP.objects.get_or_create(user=self.user)
        otp_code = otp_obj.generate_otp() 

        print(f"Generated OTP: {otp_code} for user: {self.user.email}")

        send_mail(
            subject='Password Reset OTP',
            message=f'Your OTP for password reset is: {otp_code}',
            from_email=os.getenv('EMAIL_HOST_USER'),
            recipient_list=[self.user.email],
            fail_silently=False,
        )

        return validated_data
    
class AdminForgotPasswordOTPValidateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, required=True)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User with this email does not exist.")

        otp_obj = OTP.objects.filter(user=user, otp=otp).first()
        if not otp_obj:
            raise serializers.ValidationError("Invalid OTP.")

        if otp_obj.is_expired():
            raise serializers.ValidationError("OTP has expired.")

        # Optional: Attach user or OTP object to serializer
        self.user = user
        self.otp_obj = otp_obj

        return data


class AdminForgotPasswordSetNewSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6,required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_new_password=serializers.CharField(write_only=True,required=True, min_length=8)

    def validate(self, data):
        email = data.get('email')
        otp= data.get('otp')
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')
        if new_password != confirm_new_password:
            raise serializers.ValidationError("New password and confirm password do not match.")
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User with this email does not exist.")
        otp_obj = OTP.objects.filter(user=user, otp=otp).first()
        if not otp_obj:
            raise serializers.ValidationError("Invalid OTP.")
        if otp_obj.is_expired():
            raise serializers.ValidationError("OTP has expired.")
        user.set_password(new_password)
        user.save()
        return data
        
            
        



        
class SignUpSuperUserSerializers(serializers.ModelSerializer):
    
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)


    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username']
       
       
    def create(self, data):
        password = secrets.token_urlsafe(10)  # Generate random password
        username = data.get("username")
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        
        user = User.objects.create_superuser(
            username=username,first_name=first_name, 
            last_name=last_name, password=password
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



class UserRoleFeatureSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    user_username = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()
    user_phone_number = serializers.SerializerMethodField()
    phone_number = serializers.CharField(write_only=True)
    
    
    class Meta:
        model = Roles
        fields = ['username', 'email', 'feature',
                  'user_username', 'user_email', 'phone_number', 'roles', 'user_phone_number']
        
    def get_user_username(self, obj):
        return obj.admin_user.username

    def get_user_email(self, obj):
        return obj.admin_user.email
    
    def get_user_phone_number(self, obj):
        return obj.admin_user.phone_number
    
    def validate_email(self, value):
            if CustomUser.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists.")
            return value
        
    def validate_username(self, value):
            if CustomUser.objects.filter(username=value).exists():
                raise serializers.ValidationError("Username already exists.")
            return value
    
    def validate_phone_number(self, value):
        pattern = re.compile(r"^(?:\+234|0)[789][01]\d{8}$")
        if not pattern.match(value):
            raise serializers.ValidationError("Enter a valid Nigerian phone number.")
        return value

    def create(self, validated_data):
        password = secrets.token_urlsafe(10) 
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        feature = validated_data.pop('feature')
        role = validated_data.pop('roles')
        phone_number = validated_data.pop('phone_number')
        
        user = CustomUser.objects.create_user(username=username, email=email, phone_number=phone_number, password=password)
        user.is_staff = True
        user.save() 
               
        send_mail(
            subject=f'Your Credentials to Mr:{username}',
            message=f'Your password: {password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        
        # Create the Roles entry (OneToOne)
        role_instance=Roles.objects.create(admin_user=user, roles=role, feature=feature)

        return role_instance
    
    
    
class AdminAndCustomerSerializer(serializers.ModelSerializer):
    
    admin_user = serializers.SerializerMethodField()
    customer_user = serializers.SerializerMethodField()
    incomplete_kyc = serializers.SerializerMethodField()
    
    def get_admin_user(self, instance):
        return CustomUser.objects.filter(is_staff=True, is_superuser=False).count()
        
    def get_customer_user(self, instance):
        one_week_ago = timezone.now() - timedelta(days=7)
        return CustomUser.objects.filter(is_staff=False, is_superuser=False, created_at=one_week_ago).count()
        
    def get_incomplete_kyc(self, instance):
        total=CustomUser.objects.filter(kyc_completed=False)
        return len(total)
        
    class Meta:
        model = CustomUser
        fields = ('admin_user', 'customer_user', 'incomplete_kyc')
        


class BvnRecordSerializers(serializers.ModelSerializer):
    
    verified_bvn = serializers.SerializerMethodField()
    unverified_bvn = serializers.SerializerMethodField()
    
    class Meta:
        model = BvnRecords
        fields = ['verified_bvn', 'unverified_bvn', 'attempts', 'attempted_at']
    
    
    def get_verified_bvn(self, value):
        verified = BvnRecords.objects.filter(success= True).count()
        return {'verified': verified}

    def get_unverified_bvn(self, value):
        unverified = BvnRecords.objects.filter(sucess=False).count()
        return {'unverified': unverified}
        
    def validate_bvn(self, value):
        value = str(value)
        if len(value) != 11:
            raise serializers.ValidationError('pls check the number of bvn inputed')
        
        if BvnRecords.objects.filter(bvn=value).exists():
            raise serializers.ValidationError('This bvn is active already')
        
        
    
class LoginSerializer(serializers.Serializer):
    
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError("Incorrect Login")
        
        return {'user':user}
